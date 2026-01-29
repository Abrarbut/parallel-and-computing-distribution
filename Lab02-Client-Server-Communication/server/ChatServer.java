import java.io.*;
import java.net.*;
import java.util.*;

class ClientHandler extends Thread {
    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    private String userId;
    private static Map<String, PrintWriter> clients = new HashMap<>();

    public ClientHandler(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        try {
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            out.println("Enter User ID:");
            userId = in.readLine();
            clients.put(userId, out);

            broadcast("User " + userId + " joined the chat");

            String message;
            while ((message = in.readLine()) != null) {
                if (message.startsWith("@")) {
                    String[] parts = message.split(" ", 2);
                    sendUnicast(parts[0].substring(1), parts[1]);
                } else {
                    broadcast(userId + ": " + message);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            clients.remove(userId);
            broadcast("User " + userId + " left the chat");
        }
    }

    private void broadcast(String msg) {
        for (PrintWriter writer : clients.values()) {
            writer.println(msg);
        }
    }

    private void sendUnicast(String user, String msg) {
        PrintWriter writer = clients.get(user);
        if (writer != null) {
            writer.println("(Private) " + userId + ": " + msg);
        } else {
            out.println("User not found.");
        }
    }
}

public class ChatServer {
    public static void main(String[] args) throws Exception {
        ServerSocket serverSocket = new ServerSocket(5000);
        System.out.println("Chat Server Started on port 5000");

        while (true) {
            Socket socket = serverSocket.accept();
            new ClientHandler(socket).start();
        }
    }
}
