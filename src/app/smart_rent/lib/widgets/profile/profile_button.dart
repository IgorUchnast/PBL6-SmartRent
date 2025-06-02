import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';

class SRProfileButton extends StatelessWidget {
  const SRProfileButton({
    super.key,
    required this.buttonTxt,
    required this.onPressed,
    this.isSelected = false,
  });

  final String buttonTxt;
  final VoidCallback onPressed;
  final bool isSelected;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        width: MediaQuery.of(context).size.width * 0.45,
        margin: const EdgeInsets.all(5),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isSelected ? Colors.grey[300] : Colors.white, // ✅ tu zmiana
          border: Border.all(color: SRAppColors.borderColor, width: 2),
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
        child: Text(
          buttonTxt,
          style: SRAppFonst.buttonTxt,
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
