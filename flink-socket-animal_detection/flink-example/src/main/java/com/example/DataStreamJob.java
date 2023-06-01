package com.example;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.util.Collector;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class DataStreamJob {

	public static void main(String[] args) throws Exception {
		// Set up the execution environment
		StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		// Set the Kafka properties
		Properties properties = new Properties();
		properties.setProperty("bootstrap.servers", "localhost:9092");

		// Create a Kafka consumer
		FlinkKafkaConsumer<String> kafkaConsumer = new FlinkKafkaConsumer<>(
				"input-topic", new SimpleStringSchema(), properties);

		// Create a data stream from the Kafka consumer
		DataStream<String> stream = env.addSource(kafkaConsumer);

		// Define the tumbling window with a time duration of 10 seconds
		DataStream<String> windowedStream = stream
				.windowAll(TumblingProcessingTimeWindows.of(Time.seconds(10)))
				.apply(new WindowFunction());

		// Create a Kafka producer
		FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
				"output-topic", new SimpleStringSchema(), properties);

		// Send the windowed stream to the Kafka producer
		windowedStream.addSink(kafkaProducer);

		// Execute the job
		env.execute("Tumbling Window Example");
	}

	public static class WindowFunction implements org.apache.flink.streaming.api.functions.windowing.AllWindowFunction<String, String, TimeWindow> {

		@Override
		public void apply(TimeWindow window, Iterable<String> input, Collector<String> out) {
			// Establish a TCP socket connection
			try (Socket socket = new Socket("localhost", 8888)) {
				OutputStream outputStream = socket.getOutputStream();

				// Process the messages in the window and send them to the TCP socket server
				for (String message : input) {
					// Measure the start time
					long startTime = System.currentTimeMillis();
					// Send the message to the socket server
					byte[] messageBytes = message.getBytes(StandardCharsets.UTF_8);
					outputStream.write(messageBytes);
					outputStream.flush();

					// TODO: Add code to receive and process response from the socket server
					// Example:
					 InputStream inputStream = socket.getInputStream();
					 byte[] responseBytes = new byte[1024];
					 int bytesRead = inputStream.read(responseBytes);
					 if (bytesRead > 0) {
					     String response = new String(responseBytes, 0, bytesRead);
						 // Measure the end time
						 long endTime = System.currentTimeMillis();
						 // Calculate the time taken for the response
						 long responseTime = endTime - startTime;
						 System.out.println("Response time: " + responseTime + " ms");
					     out.collect(response);
					 }
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
