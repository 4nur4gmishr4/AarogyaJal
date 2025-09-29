import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../utils/parameter_limits.dart';

class ParameterInputTile extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final String unit;
  final bool isInteger;
  final double? minValue;
  final double? maxValue;
  final IconData icon;
  final Function(String)? onChanged;

  const ParameterInputTile({
    super.key,
    required this.label,
    required this.controller,
    required this.unit,
    this.isInteger = false,
    this.minValue,
    this.maxValue,
    this.icon = Icons.science_outlined,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Material(
        elevation: 1,
        shadowColor: Colors.black12,
        borderRadius: BorderRadius.circular(16),
        color: Theme.of(context).cardColor,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    icon,
                    color: const Color(0xFF3900B3),
                    size: 20,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    label,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: controller,
                keyboardType: TextInputType.numberWithOptions(
                  decimal: !isInteger,
                  signed: false,
                ),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(
                    isInteger ? RegExp(r'[0-9]') : RegExp(r'^\d*\.?\d*'),
                  ),
                ],
                onChanged: (value) {
                  if (value.isEmpty) return;

                  final numValue = isInteger
                      ? int.tryParse(value)?.toDouble()
                      : double.tryParse(value);

                  if (numValue != null) {
                    if ((minValue != null && numValue < minValue!) ||
                        (maxValue != null && numValue > maxValue!)) {
                      // Reset to max/min if out of bounds
                      final newValue = numValue < minValue!
                          ? minValue!.toString()
                          : maxValue!.toString();
                      controller.text = newValue;
                      controller.selection = TextSelection.fromPosition(
                        TextPosition(offset: newValue.length),
                      );
                    }
                  }

                  if (onChanged != null) onChanged!(controller.text);
                },
                decoration: InputDecoration(
                  isDense: true,
                  suffixText: unit,
                  suffixStyle: TextStyle(
                    color: Theme.of(context).textTheme.bodySmall?.color,
                  ),
                  helperText: ParameterLimits.getHelperText(label),
                  helperStyle: TextStyle(
                    fontSize: 12,
                    color: Theme.of(context).textTheme.bodySmall?.color,
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide(
                      color: Theme.of(context).dividerColor,
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(
                      color: Color(0xFF3900B3),
                      width: 2,
                    ),
                  ),
                  errorBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide(
                      color: Theme.of(context).colorScheme.error,
                    ),
                  ),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'This field is required';
                  }

                  final numValue = isInteger
                      ? int.tryParse(value)?.toDouble()
                      : double.tryParse(value);

                  if (numValue == null) {
                    return 'Please enter a valid number';
                  }

                  if (minValue != null && numValue < minValue!) {
                    return 'Value must be at least ${minValue!}';
                  }

                  if (maxValue != null && numValue > maxValue!) {
                    return 'Value must be at most ${maxValue!}';
                  }

                  return null;
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
