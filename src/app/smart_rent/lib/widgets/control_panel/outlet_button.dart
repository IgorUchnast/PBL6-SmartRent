import 'package:flutter/material.dart';
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
  }

  void _onTap() {
    if (_controller.status != AnimationStatus.completed) {
      _controller.forward().then((_) {
        _controller.reverse();
        setState(() {
          isOn = !isOn;
        });
      });
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
                SizedBox(
                  height: 20,
                ),
                Divider(),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    SROutletText(
                      textData: 'Power',
                      sensorData: 20,
                    ),
                    SROutletText(
                      textData: 'Intensity',
                      sensorData: 31,
                    ),
                    SROutletText(
                      textData: 'Amparage',
                      sensorData: 24,
                    ),
                    SROutletText(
                      textData: 'Total (kWh)',
                      sensorData: 24,
                    ),
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
