    import java.io.IOException;
    import java.util.StringTokenizer;

    import org.apache.hadoop.conf.Configuration;
    import org.apache.hadoop.fs.Path;
    import org.apache.hadoop.io.IntWritable;
    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.mapreduce.Job;
    import org.apache.hadoop.mapreduce.Mapper;
    import org.apache.hadoop.mapreduce.Reducer;
    import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
    import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

    /**
     * CS332 - Distributed Computing
     * Lab 12: Hadoop MapReduce WordCount
     *
     * This program counts the number of occurrences of each word
     * in the input file using Hadoop MapReduce.
     */
    public class WordCount {

        // ---------------------------------------------------------------
        // MAPPER CLASS
        // Input:  <byte_offset, line_of_text>
        // Output: <word, 1>
        // ---------------------------------------------------------------
        public static class TokenizerMapper
                extends Mapper<Object, Text, Text, IntWritable> {

            // Constant value "1" emitted for every word
            private final static IntWritable one = new IntWritable(1);
            // Reusable Text object to hold each word
            private Text word = new Text();

            /**
             * map() is called once for each line in the input file.
             * It tokenizes the line and emits (word, 1) for each token.
             */
            @Override
            public void map(Object key, Text value, Context context)
                    throws IOException, InterruptedException {

                // Tokenize the input line
                StringTokenizer itr = new StringTokenizer(value.toString());

                while (itr.hasMoreTokens()) {
                    // Convert token to lower-case for case-insensitive count
                    word.set(itr.nextToken().toLowerCase()
                            .replaceAll("[^a-z0-9]", "")); // strip punctuation

                    // Skip empty tokens produced by punctuation stripping
                    if (!word.toString().isEmpty()) {
                        context.write(word, one);
                    }
                }
            }
        }

        // ---------------------------------------------------------------
        // REDUCER CLASS
        // Input:  <word, [1, 1, 1, ...]>   (grouped by Shuffle phase)
        // Output: <word, total_count>
        // ---------------------------------------------------------------
        public static class IntSumReducer
                extends Reducer<Text, IntWritable, Text, IntWritable> {

            private IntWritable result = new IntWritable();

            /**
             * reduce() is called once for each unique key (word).
             * It sums all the 1s associated with that word.
             */
            @Override
            public void reduce(Text key, Iterable<IntWritable> values, Context context)
                    throws IOException, InterruptedException {

                int sum = 0;
                for (IntWritable val : values) {
                    sum += val.get();
                }
                result.set(sum);
                context.write(key, result);
            }
        }

        // ---------------------------------------------------------------
        // DRIVER / MAIN
        // Configures the Job and submits it to Hadoop
        // ---------------------------------------------------------------
        public static void main(String[] args) throws Exception {

            // Validate arguments
            if (args.length != 2) {
                System.err.println("Usage: WordCount <input_path> <output_path>");
                System.exit(1);
            }

            // Create Hadoop configuration and job
            Configuration conf = new Configuration();
            Job job = Job.getInstance(conf, "Word Count");

            // Set the main class
            job.setJarByClass(WordCount.class);

            // Set Mapper and Reducer classes
            job.setMapperClass(TokenizerMapper.class);
            job.setReducerClass(IntSumReducer.class);

            // Optional: add a Combiner (acts as a local reducer to reduce
            // network traffic during the Shuffle phase)
            job.setCombinerClass(IntSumReducer.class);

            // Set output key/value types
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(IntWritable.class);

            // Set input and output paths from command-line arguments
            FileInputFormat.addInputPath(job, new Path(args[0]));
            FileOutputFormat.setOutputPath(job, new Path(args[1]));

            // Submit the job and wait for completion
            System.exit(job.waitForCompletion(true) ? 0 : 1);
        }
    }