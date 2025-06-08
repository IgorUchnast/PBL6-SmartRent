import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:http/http.dart' as http;

class DynamicSensorChart extends StatefulWidget {
  const DynamicSensorChart({super.key});

  @override
  State<DynamicSensorChart> createState() => _DynamicSensorChartState();
}

class _DynamicSensorChartState extends State<DynamicSensorChart> {
  final List<String> sensorTypes = ['temperature', 'humidity', 'power'];
  String selectedSensor = 'temperature';
  List<String> dates = [];
  List<double> values = [];

  @override
  void initState() {
    super.initState();
    fetchData(selectedSensor);
  }

  Future<void> fetchData(String type) async {
    // 🔁 Przekierowanie przez report_service
    final url = Uri.parse('http://localhost:8002/api/sensors/$type/history');
    final res = await http.get(url);

    if (res.statusCode == 200) {
      final List<dynamic> data = jsonDecode(res.body);
      setState(() {
        dates = data.map((e) => e['timestamp'] as String).toList();
        values = data.map((e) => (e['value'] as num).toDouble()).toList();
      });
    } else {
      print("Błąd: ${res.statusCode} ${res.body}");
    }
  }

  @override
  Widget build(BuildContext context) {
    final spots =
        List.generate(values.length, (i) => FlSpot(i.toDouble(), values[i]));

    return Column(
      children: [
        DropdownButton<String>(
          value: selectedSensor,
          items: sensorTypes.map((type) {
            return DropdownMenuItem(value: type, child: Text(type));
          }).toList(),
          onChanged: (value) {
            if (value != null) {
              setState(() {
                selectedSensor = value;
              });
              fetchData(value);
            }
          },
        ),
        const SizedBox(height: 20),
        SizedBox(
          height: 300,
          child: LineChart(
            LineChartData(
              titlesData: FlTitlesData(
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    interval: 1,
                    getTitlesWidget: (value, meta) {
                      int index = value.toInt();
                      return Text(index < dates.length ? dates[index] : '',
                          style: const TextStyle(fontSize: 10));
                    },
                  ),
                ),
                leftTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    getTitlesWidget: (value, _) => Text("${value.toInt()}"),
                  ),
                ),
                topTitles:
                    AxisTitles(sideTitles: SideTitles(showTitles: false)),
                rightTitles:
                    AxisTitles(sideTitles: SideTitles(showTitles: false)),
              ),
              borderData: FlBorderData(
                show: true,
                border: Border.all(color: Colors.grey),
              ),
              lineBarsData: [
                LineChartBarData(
                  spots: spots,
                  isCurved: true,
                  barWidth: 3,
                  belowBarData: BarAreaData(show: true),
                  dotData: FlDotData(show: true),
                  color: Colors.blueAccent,
                ),
              ],
              minY: values.isEmpty
                  ? 0
                  : values.reduce((a, b) => a < b ? a : b) - 1,
              maxY: values.isEmpty
                  ? 10
                  : values.reduce((a, b) => a > b ? a : b) + 1,
            ),
          ),
        ),
      ],
    );
  }
}
