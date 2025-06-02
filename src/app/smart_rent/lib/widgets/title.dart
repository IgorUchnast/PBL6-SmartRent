import 'package:flutter/material.dart';
import 'package:smart_rent/config/fonts.dart';

class SRTitle extends StatelessWidget {
  const SRTitle({
    super.key,
    required this.titleTxt,
  });

  final String titleTxt;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: Row(
        children: [
          Text(
            titleTxt,
            style: SRAppFonst.subtitle,
          ),
        ],
      ),
    );
  }
}
