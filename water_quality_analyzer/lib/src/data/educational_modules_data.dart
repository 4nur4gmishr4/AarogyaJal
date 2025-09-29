import '../models/educational_module.dart';

class EducationalModulesData {
  static final List<EducationalModule> modules = [
    EducationalModule(
      id: 'ws101',
      title: 'Water Safety Basics',
      description:
          'Learn the fundamentals of water safety and quality assessment',
      category: ModuleCategory.waterSafety,
      difficulty: ModuleDifficulty.beginner,
      thumbnailUrl: 'assets/images/water_safety.png',
      languages: ['English', 'Hindi'],
      estimatedMinutes: 30,
      contents: [
        ModuleContent(
          id: 'ws101_1',
          title: 'Understanding Water Quality',
          type: ContentType.text,
          content: '''
Water quality is essential for human health and well-being. Key parameters include:

1. Physical Parameters:
   - Temperature
   - Turbidity
   - Color and Odor

2. Chemical Parameters:
   - pH Level (Safe range: 6.5-8.5)
   - Dissolved Oxygen
   - Total Dissolved Solids

3. Biological Parameters:
   - Bacteria
   - Viruses
   - Parasites
''',
          orderIndex: 0,
        ),
        ModuleContent(
          id: 'ws101_2',
          title: 'Common Contaminants',
          type: ContentType.infographic,
          content: 'assets/images/contaminants.png',
          orderIndex: 1,
        ),
      ],
    ),
    EducationalModule(
      id: 'wp201',
      title: 'Water Purification Methods',
      description:
          'Explore various methods to purify water at home and community level',
      category: ModuleCategory.waterPurification,
      difficulty: ModuleDifficulty.intermediate,
      thumbnailUrl: 'assets/images/purification.png',
      languages: ['English', 'Hindi'],
      estimatedMinutes: 45,
      contents: [
        ModuleContent(
          id: 'wp201_1',
          title: 'Boiling Water',
          type: ContentType.text,
          content: '''
Boiling is one of the most effective water purification methods:

1. Bring water to a rolling boil
2. Maintain boiling for 1-3 minutes
3. Let it cool naturally
4. Store in clean containers

Benefits:
- Kills harmful bacteria and parasites
- Removes biological contaminants
- Simple and effective method
''',
          orderIndex: 0,
        ),
      ],
    ),
    EducationalModule(
      id: 'cs301',
      title: 'Community Sanitation',
      description:
          'Learn about community-level water management and sanitation practices',
      category: ModuleCategory.communitySanitation,
      difficulty: ModuleDifficulty.advanced,
      thumbnailUrl: 'assets/images/community.png',
      languages: ['English', 'Hindi'],
      estimatedMinutes: 60,
      contents: [
        ModuleContent(
          id: 'cs301_1',
          title: 'Water Source Protection',
          type: ContentType.text,
          content: '''
Protecting water sources is crucial for community health:

1. Source Protection Measures:
   - Maintain adequate distance from contamination sources
   - Regular cleaning and maintenance
   - Proper drainage systems

2. Community Involvement:
   - Regular monitoring
   - Reporting contamination
   - Community awareness programs
''',
          orderIndex: 0,
        ),
      ],
    ),
    EducationalModule(
      id: 'hw101',
      title: 'Handwashing and Hygiene',
      description: 'Essential practices for personal and family hygiene',
      category: ModuleCategory.handwashing,
      difficulty: ModuleDifficulty.beginner,
      thumbnailUrl: 'assets/images/handwashing.png',
      languages: ['English', 'Hindi'],
      estimatedMinutes: 25,
      contents: [
        ModuleContent(
          id: 'hw101_1',
          title: 'Proper Handwashing Steps',
          type: ContentType.text,
          content: '''
Follow these steps for effective handwashing:

1. Wet hands with clean water
2. Apply soap and create lather
3. Scrub all surfaces for 20 seconds
4. Rinse thoroughly
5. Dry with clean towel

Key Times for Handwashing:
- Before handling food
- After using the toilet
- Before eating
- After handling waste
''',
          orderIndex: 0,
        ),
      ],
    ),
  ];
}
