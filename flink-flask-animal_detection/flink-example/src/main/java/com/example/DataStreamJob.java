package com.example;

import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
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

import java.util.Properties;

import static io.restassured.RestAssured.given;

public class DataStreamJob {

	public static void main(String[] args) throws Exception {
		// Set up the execution environment
		StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		// Set the Kafka properties
		Properties properties = new Properties();
		properties.setProperty("bootstrap.servers", "10.15.206.130:9092");

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
			RequestSpecification request  = given();
			Response response;
			// Process the messages in the window and send the result to the collector
			// You can perform any custom processing logic here
			for (String message : input) {
				request.header("Content-Type", ContentType.JSON);
				request.body(message);
				response = request.post("http://10.15.206.130:5000/result");
				out.collect(response.asString());
			}
		}
	}
}