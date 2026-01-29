import java.io.*;
import java.net.*;
import java.util.*;

class ClientHandler extends Thread {
    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    private String userId;

    // Thread-safe map of clients
    private static Map<String, PrintWriter> clients = Collections.synchronizedMap(new HashMap<>());

    public ClientHandler(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        try {
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            // Ask for user ID
            out.println("Enter User ID:");
            userId = in.readLine().trim(); // removes extra spaces
            clients.put(userId, out);

            // Check for duplicate user ID
            if (clients.containsKey(userId)) {
                out.println("User ID already taken. Connection closed.");
                socket.close();
                return;
            }

            clients.put(userId, out);
            broadcast("User " + userId + " joined the chat");

            String message;
            while ((message = in.readLine()) != null) {
                if (message.startsWith("@")) {
                    // Private message
                    String[] parts = message.split(" ", 2);
                    if (parts.length >= 2) {
                        sendUnicast(parts[0].substring(1), parts[1]);
                    } else {
                        out.println("Invalid private message format. Use: @userId message");
                    }
                } else {
                    // Broadcast to all
                    broadcast(userId + ": " + message);
                }
            }
        } catch (IOException e) {
            System.out.println("Connection error with user " + userId);
        } finally {
            try {
                if (userId != null) {
                    clients.remove(userId);
                    broadcast("User " + userId + " left the chat");
                }
                if (socket != null)
                    socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Broadcast to all clients
    private void broadcast(String msg) {
        synchronized (clients) {
            for (PrintWriter writer : clients.values()) {
                writer.println(msg);
            }
        }
    }

    // Send message to a specific user only
    private void sendUnicast(String recipient, String msg) {
        PrintWriter writer = clients.get(recipient);
        if (writer != null) {
            writer.println("(Private) " + userId + ": " + msg);
            out.println("(Private to " + recipient + "): " + msg); // optional echo to sender
        } else {
            out.println("User '" + recipient + "' not found.");
        }
    }
}

public class ChatServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(5000);
        System.out.println("Chat Server Started on port 5000");

        while (true) {
            Socket socket = serverSocket.accept();
            new ClientHandler(socket).start();
        }
    }
}
