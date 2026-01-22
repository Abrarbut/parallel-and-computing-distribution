public class SingleThreadPI {

    public static void main(String[] args) {
        long startTime = System.nanoTime();

        int iterations = 100_000_000;
        double pi = 0.0;
        double sign = 1.0;

        for (int i = 0; i < iterations; i++) {
            pi += sign / (2.0 * i + 1.0);
            sign = -sign;
        }

        pi *= 4;

        long endTime = System.nanoTime();
        double executionTime = (endTime - startTime) / 1_000_000.0;

        System.out.println("PI (Single Thread) = " + pi);
        System.out.println("Execution Time = " + executionTime + " ms");
    }
}
 