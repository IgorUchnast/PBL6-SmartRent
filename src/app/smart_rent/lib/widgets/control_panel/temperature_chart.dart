import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class SRTemperatureChart extends StatelessWidget {
  // Przykładowe dane – do łatwego zastąpienia w przyszłości
  final List<String> dates = [
    '26.05',
    '27.05',
    '28.05',
    '29.05',
    '30.05',
    '31.05',
    '01.06'
  ];

  final List<double> temperatures = [21.5, 23.0, 19.8, 22.1, 24.3, 25.6, 23.9];

  SRTemperatureChart({super.key});

  @override
  Widget build(BuildContext context) {
    List<FlSpot> temperatureSpots = List.generate(
      temperatures.length,
      (index) => FlSpot(index.toDouble(), temperatures[index]),
    );

    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: SizedBox(
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
                    return Padding(
                      padding: const EdgeInsets.only(top: 8.0),
                      child: Text(
                        index < dates.length ? dates[index] : '',
                        style: TextStyle(fontSize: 12),
                      ),
                    );
                  },
                ),
              ),
              leftTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  interval: 1,
                  getTitlesWidget: (value, meta) {
                    return Text('${value.toInt()}°',
                        style: TextStyle(fontSize: 12));
                  },
                ),
              ),
              rightTitles:
                  AxisTitles(sideTitles: SideTitles(showTitles: false)),
              topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
            ),
            gridData: FlGridData(
              show: true,
              drawVerticalLine: true,
              horizontalInterval: 1,
              verticalInterval: 1,
              getDrawingHorizontalLine: (_) => FlLine(
                color: Colors.grey.shade300,
                strokeWidth: 1,
              ),
              getDrawingVerticalLine: (_) => FlLine(
                color: Colors.grey.shade300,
                strokeWidth: 1,
              ),
            ),
            borderData: FlBorderData(
              show: true,
              border: Border.all(color: Colors.grey.shade400),
            ),
            lineBarsData: [
              LineChartBarData(
                spots: temperatureSpots,
                isCurved: true,
                barWidth: 3,
                dotData: FlDotData(show: true),
                belowBarData: BarAreaData(
                  show: true,
                  gradient: LinearGradient(
                    colors: [
                      Colors.blueAccent.withOpacity(0.3),
                      Colors.transparent
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
                color: Colors.blueAccent,
              ),
            ],
            minY: temperatures.reduce((a, b) => a < b ? a : b) - 1,
            maxY: temperatures.reduce((a, b) => a > b ? a : b) + 1,
          ),
        ),
      ),
    );
  }
}
