import 'package:flutter/material.dart';
import '../models/educational_module.dart';
import '../widgets/custom_app_bar.dart';
import 'content_detail_screen.dart';

class ModuleDetailScreen extends StatelessWidget {
  final EducationalModule module;

  const ModuleDetailScreen({
    super.key,
    required this.module,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: module.title,
        showBackButton: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AspectRatio(
              aspectRatio: 16 / 9,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(
                  module.thumbnailUrl,
                  fit: BoxFit.cover,
                ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                _buildInfoChip(
                  Icons.timer_outlined,
                  '${module.estimatedMinutes} min',
                ),
                const SizedBox(width: 8),
                _buildInfoChip(
                  Icons.bar_chart,
                  _getDifficultyText(module.difficulty),
                ),
                const SizedBox(width: 8),
                _buildInfoChip(
                  Icons.language,
                  module.languages.join(', '),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Text(
              'About This Module',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              module.description,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 24),
            Text(
              'Contents',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: module.contents.length,
              itemBuilder: (context, index) {
                final content = module.contents[index];
                return Card(
                  child: ListTile(
                    onTap: () => _openContent(context, content),
                    leading: CircleAvatar(
                      backgroundColor: const Color(0xFF3900B3).withOpacity(0.1),
                      child: Text(
                        '${index + 1}',
                        style: const TextStyle(
                          color: Color(0xFF3900B3),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    title: Text(content.title),
                    subtitle: Text(_getContentTypeText(content.type)),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoChip(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: const Color(0xFF3900B3).withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 16,
            color: const Color(0xFF3900B3),
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: const TextStyle(
              color: Color(0xFF3900B3),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  String _getDifficultyText(ModuleDifficulty difficulty) {
    switch (difficulty) {
      case ModuleDifficulty.beginner:
        return 'Beginner';
      case ModuleDifficulty.intermediate:
        return 'Intermediate';
      case ModuleDifficulty.advanced:
        return 'Advanced';
    }
  }

  String _getContentTypeText(ContentType type) {
    switch (type) {
      case ContentType.video:
        return 'Video';
      case ContentType.audio:
        return 'Audio';
      case ContentType.text:
        return 'Reading';
      case ContentType.infographic:
        return 'Infographic';
      case ContentType.quiz:
        return 'Quiz';
      case ContentType.interactive:
        return 'Interactive';
    }
  }

  void _openContent(BuildContext context, ModuleContent content) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ContentDetailScreen(content: content),
      ),
    );
  }
}
