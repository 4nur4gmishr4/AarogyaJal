import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:ui';

class CustomBottomNavBar extends StatefulWidget {
  final Function(int) onTap;
  final int currentIndex;

  const CustomBottomNavBar({
    Key? key,
    required this.onTap,
    this.currentIndex = 0,
  }) : super(key: key);

  @override
  State<CustomBottomNavBar> createState() => _CustomBottomNavBarState();
}

class _CustomBottomNavBarState extends State<CustomBottomNavBar> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // Safe area bottom padding
    final bottomPadding = MediaQuery.of(context).padding.bottom;

    return Container(
      height: 75 + bottomPadding, // Increased height
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 0),
      padding:
          EdgeInsets.only(bottom: bottomPadding), // Add padding for safe area
      child: Stack(
        alignment: Alignment.center,
        children: [
          // Main glassmorphic container
          ClipRRect(
            borderRadius: BorderRadius.circular(25),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                height: 75,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.85),
                  borderRadius: BorderRadius.circular(25),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.3),
                    width: 1,
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildNavItem(0, Icons.home_rounded, 'Home'),
                    _buildNavItem(1, Icons.bar_chart_rounded, 'Statistics'),
                    Transform.translate(
                      offset:
                          const Offset(0, 0), // Adjusted to show full circle
                      child: Container(
                        width: 56,
                        height: 56,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0xFF3700B3).withOpacity(0.3),
                              blurRadius: 12,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: Hero(
                          tag: 'chatbot_button',
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              customBorder: const CircleBorder(),
                              onTap: () => widget.onTap(2),
                              child: Ink(
                                decoration: const BoxDecoration(
                                  shape: BoxShape.circle,
                                  color: Color(0xFF3700B3),
                                ),
                                child: const Icon(
                                  Icons.smart_toy,
                                  color: Colors.white,
                                  size: 28,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                    _buildNavItem(3, Icons.school_rounded, 'Learn'),
                    _buildNavItem(4, Icons.person_rounded, 'Profile'),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem(int index, IconData icon, String label) {
    final isSelected = widget.currentIndex == index;

    return GestureDetector(
      onTap: () {
        if (!isSelected) {
          HapticFeedback.selectionClick();
          widget.onTap(index);
        }
      },
      child: SizedBox(
        width: 70,
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Background highlight
            AnimatedOpacity(
              duration: const Duration(milliseconds: 200),
              opacity: isSelected ? 1.0 : 0.0,
              child: Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(18),
                  color: Colors.grey.shade200.withOpacity(0.8),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04),
                      blurRadius: 4,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
              ),
            ),
            // Icon and label
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TweenAnimationBuilder<double>(
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeOutCubic,
                  tween: Tween<double>(
                    begin: 0.0,
                    end: isSelected ? 1.0 : 0.0,
                  ),
                  builder: (context, value, child) {
                    return Transform.translate(
                      offset: Offset(
                          0,
                          2 +
                              (-2 *
                                  value)), // Moved down by default, moves up when selected
                      child: Transform.scale(
                        scale: 1.0 + (0.2 * value), // Scale up when selected
                        child: Icon(
                          icon,
                          color:
                              isSelected ? Colors.black : Colors.grey.shade600,
                          size: 26, // Slightly larger icons
                        ),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 6),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
                    color: isSelected ? Colors.black : Colors.grey.shade600,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
