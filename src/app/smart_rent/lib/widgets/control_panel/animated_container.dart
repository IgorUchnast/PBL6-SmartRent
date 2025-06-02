import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/widgets/control_panel/device_list.dart';
import 'package:smart_rent/widgets/title.dart';

class ExpandableOutletSection extends StatefulWidget {
  const ExpandableOutletSection({
    super.key,
    required this.sectionName,
    required this.sectionContainer,
    required this.deviceList,
  });
  final String sectionName;
  final Widget sectionContainer;
  final List<Device> deviceList;

  @override
  State<ExpandableOutletSection> createState() =>
      _ExpandableOutletSectionState();
}

class _ExpandableOutletSectionState extends State<ExpandableOutletSection> {
  bool _isExpanded = false;

  void _toggleExpand() {
    setState(() {
      _isExpanded = !_isExpanded;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      child: Column(
        children: [
          GestureDetector(
            onTap: _toggleExpand,
            child: Container(
              decoration: BoxDecoration(
                color: SRAppColors.backgroundColor,
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
              padding: const EdgeInsets.all(12),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      SRTitle(titleTxt: widget.sectionName),
                      Row(
                        children: [
                          DeviceDropdownPage(
                            deviceList: widget.deviceList,
                          ),
                          const SizedBox(width: 8),
                          AnimatedRotation(
                            turns: _isExpanded ? 0.5 : 0.0,
                            duration: const Duration(milliseconds: 200),
                            child: Icon(
                              _isExpanded
                                  ? Icons.keyboard_arrow_up
                                  : Icons.keyboard_arrow_down,
                              size: 28,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  AnimatedSwitcher(
                    duration: const Duration(milliseconds: 300),
                    child: _isExpanded
                        ? widget.sectionContainer
                        : const SizedBox.shrink(),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
