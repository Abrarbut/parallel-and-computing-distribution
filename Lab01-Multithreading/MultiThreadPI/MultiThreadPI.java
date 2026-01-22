class PiThread extends Thread {
    private int start, end;
    private double result = 0.0;

    public PiThread(int start, int end) {
        this.start = start;
        this.end = end;
    }

    public void run() {
        double sign = (start % 2 == 0) ? 1.0 : -1.0;

        for (int i = start; i < end; i++) {
            result += sign / (2.0 * i + 1.0);
            sign = -sign;
        }
    }

    public double getResult() {
        return result;
    }
}

public class MultiThreadPI {

    public static void main(String[] args) throws InterruptedException {
        long startTime = System.nanoTime();

        int iterations = 100_000_000;
        int mid = iterations / 2;

        PiThread t1 = new PiThread(0, mid);
        PiThread t2 = new PiThread(mid, iterations);

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        double pi = 4 * (t1.getResult() + t2.getResult());

        long endTime = System.nanoTime();
        double executionTime = (endTime - startTime) / 1_000_000.0;

        System.out.println("PI (Multi Thread) = " + pi);
        System.out.println("Execution Time = " + executionTime + " ms");
    }
}
