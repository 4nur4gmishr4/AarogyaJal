import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final bool showBackButton;
  final List<Widget>? additionalActions;
  final double elevation;
  final bool showLogo;

  const CustomAppBar({
    super.key,
    required this.title,
    this.showBackButton = true,
    this.additionalActions,
    this.elevation = 2,
    this.showLogo = true,
  });

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: const Color(0xFF3700b3),
      elevation: elevation,
      systemOverlayStyle: SystemUiOverlayStyle.light,
      centerTitle: false,
      automaticallyImplyLeading: showBackButton,
      leading: showBackButton
          ? IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.of(context).pop(),
            )
          : null,
      title: Row(
        children: [
          if (showLogo)
            Container(
              height: 32,
              width: 32,
              margin: const EdgeInsets.only(right: 12),
              child: Image.asset(
                'AppLogo/INSIDELOGO.png',
                fit: BoxFit.contain,
              ),
            ),
          Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
      actions: [
        ...(additionalActions ?? []),
        IconButton(
          icon: const Icon(Icons.notifications_outlined),
          color: Colors.white,
          onPressed: () {
            // Show notifications
          },
        ),
        IconButton(
          icon: const Icon(Icons.help_outline),
          color: Colors.white,
          onPressed: () {
            // Show help dialog
          },
        ),
        IconButton(
          icon: const Icon(Icons.settings_outlined),
          color: Colors.white,
          onPressed: () {
            // Open settings
          },
        ),
      ],
    );
  }
}
