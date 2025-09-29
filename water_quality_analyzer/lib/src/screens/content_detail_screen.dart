import 'package:flutter/material.dart';
import '../models/educational_module.dart';
import '../widgets/custom_app_bar.dart';

class ContentDetailScreen extends StatelessWidget {
  final ModuleContent content;

  const ContentDetailScreen({
    super.key,
    required this.content,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: content.title,
        showBackButton: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (content.type == ContentType.text) ...[
              Card(
                elevation: 2,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    content.content,
                    style: const TextStyle(
                      fontSize: 16,
                      height: 1.5,
                    ),
                  ),
                ),
              ),
            ] else if (content.type == ContentType.infographic) ...[
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(
                  content.content,
                  fit: BoxFit.cover,
                ),
              ),
            ] else if (content.type == ContentType.video) ...[
              // TODO: Implement video player
              const Center(
                child: Text('Video content coming soon'),
              ),
            ] else if (content.type == ContentType.interactive) ...[
              // TODO: Implement interactive content
              const Center(
                child: Text('Interactive content coming soon'),
              ),
            ],
            const SizedBox(height: 24),
            if (content.type == ContentType.text)
              ElevatedButton.icon(
                onPressed: () {
                  // TODO: Implement text-to-speech
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF3900B3),
                  padding: const EdgeInsets.symmetric(
                    horizontal: 24,
                    vertical: 12,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                icon: const Icon(Icons.volume_up_outlined),
                label: const Text('Read Aloud'),
              ),
          ],
        ),
      ),
    );
  }
}
