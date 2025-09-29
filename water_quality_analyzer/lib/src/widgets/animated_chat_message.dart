import 'package:flutter/material.dart';

class AnimatedChatMessage extends StatelessWidget {
  final String text;
  final bool isUser;
  final bool isNew;

  const AnimatedChatMessage({
    super.key,
    required this.text,
    required this.isUser,
    this.isNew = false,
  });

  @override
  Widget build(BuildContext context) {
    Widget messageContent = Container(
      margin: const EdgeInsets.symmetric(vertical: 10.0),
      child: Row(
        mainAxisAlignment:
            isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            Container(
              margin: const EdgeInsets.only(right: 16.0, top: 18.0),
              child: const CircleAvatar(
                backgroundColor: Color(0xFF3700B3),
                radius: 20.0,
                child: Icon(
                  Icons.smart_toy,
                  color: Colors.white,
                  size: 22.0,
                ),
              ),
            ),
          ],
          Flexible(
            child: Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
              decoration: BoxDecoration(
                color: isUser ? const Color(0xFF3700B3) : Colors.grey[200],
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(!isUser ? 0 : 18.0),
                  topRight: Radius.circular(isUser ? 0 : 18.0),
                  bottomLeft: const Radius.circular(18.0),
                  bottomRight: const Radius.circular(18.0),
                ),
                boxShadow: [
                  BoxShadow(
                    offset: const Offset(0, 2),
                    blurRadius: 4,
                    color: Colors.black.withOpacity(0.1),
                  ),
                ],
              ),
              child: Text(
                text,
                style: TextStyle(
                  color: isUser ? Colors.white : Colors.black87,
                ),
              ),
            ),
          ),
          if (isUser) ...[
            Container(
              margin: const EdgeInsets.only(left: 16.0, top: 5.0),
              child: const CircleAvatar(
                radius: 20.0,
                child: Icon(
                  Icons.person,
                  size: 22.0,
                ),
              ),
            ),
          ],
        ],
      ),
    );

    if (isNew) {
      return TweenAnimationBuilder<double>(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOutQuint,
        tween: Tween(begin: 0.0, end: 1.0),
        builder: (context, value, child) {
          return Transform.scale(
            scale: 0.5 + (value * 0.5),
            child: Transform.translate(
              offset: Offset(
                (isUser ? 1.0 : -1.0) * (1.0 - value) * 30,
                (1.0 - value) * 20,
              ),
              child: Opacity(
                opacity: value,
                child: child,
              ),
            ),
          );
        },
        child: messageContent,
      );
    }

    return messageContent;
  }
}
