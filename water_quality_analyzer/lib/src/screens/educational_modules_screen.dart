import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/educational_module.dart';
import '../providers/educational_module_provider.dart';
import '../widgets/module_card.dart';
import '../widgets/category_selector.dart';
import '../widgets/achievement_banner.dart';
import '../widgets/custom_app_bar.dart';
import 'module_detail_screen.dart';

class EducationalModulesScreen extends StatefulWidget {
  const EducationalModulesScreen({Key? key}) : super(key: key);

  @override
  State<EducationalModulesScreen> createState() =>
      _EducationalModulesScreenState();
}

class _EducationalModulesScreenState extends State<EducationalModulesScreen> {
  ModuleCategory _selectedCategory = ModuleCategory.waterSafety;

  @override
  Widget build(BuildContext context) {
    return Consumer<EducationalModuleProvider>(
      builder: (context, provider, child) {
        return Scaffold(
          appBar: CustomAppBar(
            title: 'Educational Modules',
            showBackButton: false,
            additionalActions: [
              IconButton(
                icon: Icon(
                    provider.isOfflineMode ? Icons.cloud_off : Icons.cloud),
                onPressed: () => provider.toggleOfflineMode(),
              ),
              PopupMenuButton<String>(
                icon: const Icon(Icons.language),
                onSelected: (String language) => provider.setLanguage(language),
                itemBuilder: (BuildContext context) => [
                  const PopupMenuItem(value: 'en', child: Text('English')),
                  const PopupMenuItem(value: 'hi', child: Text('हिंदी')),
                  const PopupMenuItem(value: 'bn', child: Text('বাংলা')),
                  const PopupMenuItem(value: 'as', child: Text('অসমীয়া')),
                ],
              ),
            ],
          ),
          body: Column(
            children: [
              AchievementBanner(
                achievements: provider.getUnlockedAchievements(),
              ),
              CategorySelector(
                selectedCategory: _selectedCategory,
                onCategorySelected: (category) {
                  setState(() => _selectedCategory = category);
                },
              ),
              Expanded(
                child: GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    childAspectRatio: 0.75,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                  ),
                  itemCount:
                      provider.getModulesByCategory(_selectedCategory).length,
                  itemBuilder: (context, index) {
                    final module =
                        provider.getModulesByCategory(_selectedCategory)[index];
                    return ModuleCard(
                      module: module,
                      onTap: () => _openModule(context, module),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _openModule(BuildContext context, EducationalModule module) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ModuleDetailScreen(module: module),
      ),
    );
  }
}
