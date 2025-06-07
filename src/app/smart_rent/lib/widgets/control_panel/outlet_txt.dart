import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';

class SROutletText extends StatelessWidget {
  const SROutletText({
    super.key,
    required this.textData,
    required this.sensorData,
  });

  final String textData;
  final double sensorData;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(5.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            textData,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.bold,
              color: SRAppColors.firstFontColor,
            ),
          ),
          Text(
            '$sensorData',
            style: TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.normal,
              color: SRAppColors.firstFontColor,
            ),
          ),
        ],
      ),
    );
  }
}
