import 'package:flutter/material.dart';
import 'package:smart_rent/config/fonts.dart';

class SRSubTitle extends StatelessWidget {
  const SRSubTitle({
    super.key,
    required this.titleTxt,
  });

  final String titleTxt;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(5.0),
      child: Text(
        titleTxt,
        style: SRAppFonst.subsubtitle,
      ),
    );
  }
}
