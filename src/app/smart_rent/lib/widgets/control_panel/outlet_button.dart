import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:smart_rent/api/config.dart';
import 'dart:convert';
import 'package:smart_rent/widgets/control_panel/outlet_txt.dart';

class SRPowerButtonScreen extends StatefulWidget {
  const SRPowerButtonScreen({super.key});

  @override
  State<SRPowerButtonScreen> createState() => _SRPowerButtonScreenState();
}

class _SRPowerButtonScreenState extends State<SRPowerButtonScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  bool isOn = false;
  double powerConsumption = 0.0;
  double voltage = 0.0;
  double amparage = 0.0;
  double total = 0.0;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
      lowerBound: 0.0,
      upperBound: 0.1,
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.9).animate(_controller);

    _fetchOutletData();
    _fetchSensorData();
  }

  Future<void> _fetchOutletData() async {
    try {
      final data = await fetchOutletStatus(1);
      setState(() {
        isOn = data['status'] == 'on';
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Błąd pobierania danych gniazdka')),
      );
    }
  }

  Future<Map<String, dynamic>> fetchOutletStatus(int outletId) async {
    final response = await http.get(
      Uri.parse('$service2/api/outlets/$outletId/status'),
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to fetch outlet status');
    }
  }

  Future<void> toggleOutletStatus(int outletId) async {
    final response = await http.post(
      Uri.parse('$service2/api/outlets/$outletId/toggle'),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to toggle outlet');
    }
  }

  Future<void> _fetchSensorData() async {
    try {
      powerConsumption = await fetchLatestSensorValue('power');
      voltage = await fetchLatestSensorValue('voltage');
      amparage = await fetchLatestSensorValue('amperage');
      total = await fetchLatestSensorValue('total');

      setState(() {});
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Błąd pobierania danych z czujników')),
      );
    }
  }

  Future<double> fetchLatestSensorValue(String type) async {
    final response = await http.get(
      Uri.parse('$service2/api/sensors/$type/latest'),
    );

    if (response.statusCode == 200) {
      final jsonBody = json.decode(response.body);
      return jsonBody['value']?.toDouble() ?? 0.0;
    } else {
      throw Exception('Failed to fetch $type data');
    }
  }

  void _onTap() async {
    if (_controller.status != AnimationStatus.completed) {
      await _controller.forward();
      await _controller.reverse();

      try {
        await toggleOutletStatus(1);
        await _fetchOutletData();
        await _fetchSensorData();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Błąd zmiany stanu gniazdka')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: GestureDetector(
          onTap: _onTap,
          child: AnimatedBuilder(
            animation: _scaleAnimation,
            builder: (context, child) => Transform.scale(
              scale: _scaleAnimation.value,
              child: child,
            ),
            child: Column(
              children: [
                Container(
                  height: 200,
                  width: 200,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isOn
                        ? const Color.fromARGB(255, 146, 255, 92)
                        : Colors.grey[300],
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.2),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Icon(
                    Icons.power_settings_new,
                    size: 100,
                    color: isOn ? Colors.white : Colors.black,
                  ),
                ),
                const SizedBox(height: 20),
                const Divider(),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    SROutletText(
                        textData: 'Power (W)', sensorData: powerConsumption),
                    SROutletText(textData: 'Voltage (V)', sensorData: voltage),
                    SROutletText(
                        textData: 'Amperage (A)', sensorData: amparage),
                    // SROutletText(textData: 'Total (kWh)', sensorData: total),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
