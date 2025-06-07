import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/subtitle.dart';

class SRProfileContainer extends StatelessWidget {
  const SRProfileContainer({
    super.key,
    required this.userName,
    required this.userEmail,
  });

  final String userEmail;
  final String userName;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(
          color: SRAppColors.borderColor,
          width: 2,
        ),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            spreadRadius: 2,
            blurRadius: 6,
            offset: const Offset(2, 4),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.max,
        children: [
          Row(
            children: [
              SRSubTitle(titleTxt: "Name:"),
              Text(
                userName,
                style: SRAppFonst.darkTxt,
              ),
            ],
          ),
          Row(
            children: [
              SRSubTitle(titleTxt: "Email:"),
              Text(
                userEmail,
                style: SRAppFonst.darkTxt,
              ),
            ],
          )
        ],
      ),
    );
  }
}
