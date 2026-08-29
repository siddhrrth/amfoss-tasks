import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const OnePieceMemoryMatcher());
}

// ============================================================
// APP
// ============================================================

class OnePieceMemoryMatcher extends StatefulWidget {
  const OnePieceMemoryMatcher({super.key});

  @override
  State<OnePieceMemoryMatcher> createState() =>
      _OnePieceMemoryMatcherState();
}

class _OnePieceMemoryMatcherState extends State<OnePieceMemoryMatcher> {
  ThemeMode _themeMode = ThemeMode.dark;

  @override
  void initState() {
    super.initState();
    _loadTheme();
  }

  Future<void> _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    final dark = prefs.getBool('darkMode') ?? true;

    if (!mounted) return;

    setState(() {
      _themeMode = dark ? ThemeMode.dark : ThemeMode.light;
    });
  }

  Future<void> _toggleTheme() async {
    final newDark = _themeMode != ThemeMode.dark;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('darkMode', newDark);

    if (!mounted) return;

    setState(() {
      _themeMode = newDark ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'One Piece Memory Matcher',
      themeMode: _themeMode,

      // ========================================================
      // LIGHT THEME
      // ========================================================

      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.light,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE09A2D),
          brightness: Brightness.light,
        ),
        scaffoldBackgroundColor: const Color(0xFFF6F1E8),
        fontFamily: 'Arial',
      ),

      // ========================================================
      // DARK THEME
      // ========================================================

      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE09A2D),
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFF080B10),
        fontFamily: 'Arial',
      ),

      home: MemoryGamePage(
        isDarkMode: _themeMode == ThemeMode.dark,
        onToggleTheme: _toggleTheme,
      ),
    );
  }
}

// ============================================================
// CARD MODEL
// ============================================================

class MemoryCard {
  final String character;

  bool isFaceUp;
  bool isMatched;

  MemoryCard({
    required this.character,
    this.isFaceUp = false,
    this.isMatched = false,
  });
}

// ============================================================
// GAME PAGE
// ============================================================

class MemoryGamePage extends StatefulWidget {
  final bool isDarkMode;
  final VoidCallback onToggleTheme;

  const MemoryGamePage({
    super.key,
    required this.isDarkMode,
    required this.onToggleTheme,
  });

  @override
  State<MemoryGamePage> createState() => _MemoryGamePageState();
}

class _MemoryGamePageState extends State<MemoryGamePage> {
  final Random _random = Random();

  // ==========================================================
  // CHARACTER LIST
  // ==========================================================

  final List<String> _characters = [
    'luffy',
    'zoro',
    'nami',
    'sanji',
    'chopper',
    'robin',
    'usopp',
    'ace',
  ];

  List<MemoryCard> _cards = [];

  int _firstIndex = -1;
  int _secondIndex = -1;

  int _moves = 0;
  int _score = 0;
  int _seconds = 0;
  int _bestScore = 0;

  bool _isBusy = false;
  bool _gameStarted = false;

  Timer? _timer;

  // ============================================================
  // LIFECYCLE
  // ============================================================

  @override
  void initState() {
    super.initState();

    _loadBestScore();
    _startNewGame();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  // ============================================================
  // PERSISTENCE
  // ============================================================

  Future<void> _loadBestScore() async {
    final prefs = await SharedPreferences.getInstance();

    if (!mounted) return;

    setState(() {
      _bestScore = prefs.getInt('bestScore') ?? 0;
    });
  }

  Future<void> _saveBestScore() async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.setInt(
      'bestScore',
      _bestScore,
    );
  }

  // ============================================================
  // START NEW GAME
  // ============================================================

  void _startNewGame() {
    _timer?.cancel();

    final shuffled = [
      ..._characters,
      ..._characters,
    ];

    shuffled.shuffle(_random);

    setState(() {
      _cards = shuffled
          .map(
            (character) => MemoryCard(
              character: character,
            ),
          )
          .toList();

      _firstIndex = -1;
      _secondIndex = -1;

      _moves = 0;
      _score = 0;
      _seconds = 0;

      _isBusy = false;
      _gameStarted = false;
    });
  }

  // ============================================================
  // TIMER
  // ============================================================

  void _startTimer() {
    _timer?.cancel();

    _timer = Timer.periodic(
      const Duration(seconds: 1),
      (_) {
        if (!mounted || !_gameStarted) return;

        setState(() {
          _seconds++;
        });
      },
    );
  }

  // ============================================================
  // CARD TAP
  // ============================================================

  void _handleCardTap(int index) {
    if (_isBusy) return;

    final card = _cards[index];

    if (card.isFaceUp || card.isMatched) {
      return;
    }

    // Start timer on first card.
    if (!_gameStarted) {
      setState(() {
        _gameStarted = true;
      });

      _startTimer();
    }

    setState(() {
      card.isFaceUp = true;
    });

    // First card.
    if (_firstIndex == -1) {
      setState(() {
        _firstIndex = index;
      });

      return;
    }

    // Second card.
    setState(() {
      _secondIndex = index;
      _moves++;
      _isBusy = true;
    });

    _checkMatch();
  }

  // ============================================================
  // CHECK MATCH
  // ============================================================

  Future<void> _checkMatch() async {
    final first = _cards[_firstIndex];
    final second = _cards[_secondIndex];

    await Future.delayed(
      const Duration(milliseconds: 650),
    );

    if (!mounted) return;

    if (first.character == second.character) {
      setState(() {
        first.isMatched = true;
        second.isMatched = true;

        _score += 100;
      });
    } else {
      setState(() {
        first.isFaceUp = false;
        second.isFaceUp = false;

        if (_score >= 15) {
          _score -= 15;
        }
      });
    }

    setState(() {
      _firstIndex = -1;
      _secondIndex = -1;
      _isBusy = false;
    });

    if (_cards.every((card) => card.isMatched)) {
      _finishGame();
    }
  }

  // ============================================================
  // FINISH GAME
  // ============================================================

  Future<void> _finishGame() async {
    _timer?.cancel();

    final timeBonus = max(
      0,
      500 - (_seconds * 5),
    );

    final moveBonus = max(
      0,
      500 - (_moves * 20),
    );

    final finalScore = _score + timeBonus + moveBonus;

    setState(() {
      _score = finalScore;
      _gameStarted = false;
    });

    final isNewBest = finalScore > _bestScore;

    if (isNewBest) {
      setState(() {
        _bestScore = finalScore;
      });

      await _saveBestScore();
    }

    if (!mounted) return;

    _showGameOverDialog(isNewBest);
  }

  // ============================================================
  // GAME OVER DIALOG
  // ============================================================

  void _showGameOverDialog(bool isNewBest) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          title: Column(
            children: [
              Text(
                isNewBest ? '🏆' : '☠️',
                style: const TextStyle(
                  fontSize: 42,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                isNewBest
                    ? 'NEW BEST SCORE!'
                    : 'GRAND LINE CLEARED!',
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontWeight: FontWeight.w900,
                  letterSpacing: 1,
                ),
              ),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                '$_score',
                style: TextStyle(
                  fontSize: 42,
                  fontWeight: FontWeight.w900,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              const SizedBox(height: 16),
              _resultRow(
                Icons.touch_app_rounded,
                'Moves',
                '$_moves',
              ),
              const SizedBox(height: 8),
              _resultRow(
                Icons.timer_outlined,
                'Time',
                _formatTime(_seconds),
              ),
            ],
          ),
          actions: [
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: () {
                  Navigator.pop(context);
                  _startNewGame();
                },
                icon: const Icon(Icons.refresh_rounded),
                label: const Text('PLAY AGAIN'),
              ),
            ),
          ],
        );
      },
    );
  }

  // ============================================================
  // RESULT ROW
  // ============================================================

  Widget _resultRow(
    IconData icon,
    String label,
    String value,
  ) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(
          icon,
          size: 20,
          color: Theme.of(context).colorScheme.primary,
        ),
        const SizedBox(width: 8),
        Text(
          '$label: ',
          style: const TextStyle(
            fontWeight: FontWeight.w600,
          ),
        ),
        Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.w900,
          ),
        ),
      ],
    );
  }

  // ============================================================
  // FORMAT TIME
  // ============================================================

  String _formatTime(int seconds) {
    final minutes = seconds ~/ 60;
    final remaining = seconds % 60;

    return '${minutes.toString().padLeft(2, '0')}:'
        '${remaining.toString().padLeft(2, '0')}';
  }

  // ============================================================
  // MAIN UI
  // ============================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final width = constraints.maxWidth;
            final height = constraints.maxHeight;

            final isMobile = width < 750;
            final isShort = height < 700;

            final horizontalPadding = isMobile ? 14.0 : 28.0;
            final verticalPadding = isShort ? 6.0 : 14.0;

            return Padding(
              padding: EdgeInsets.symmetric(
                horizontal: horizontalPadding,
                vertical: verticalPadding,
              ),
              child: Column(
                children: [
                  // ------------------------------------------------
                  // TOP BAR
                  // ------------------------------------------------

                  _buildTopBar(),

                  SizedBox(
                    height: isShort ? 6 : 12,
                  ),

                  // ------------------------------------------------
                  // HERO
                  // ------------------------------------------------

                  _buildHero(),

                  SizedBox(
                    height: isShort ? 7 : 14,
                  ),

                  // ------------------------------------------------
                  // MAIN GAME AREA
                  // ------------------------------------------------

                  Expanded(
                    child: isMobile
                        ? _buildMobileGameLayout()
                        : _buildDesktopGameLayout(),
                  ),

                  SizedBox(
                    height: isShort ? 6 : 12,
                  ),

                  // ------------------------------------------------
                  // NEW GAME
                  // ------------------------------------------------

                  _buildNewGameButton(
                    compact: isShort,
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  // ============================================================
  // DESKTOP GAME LAYOUT
  // ============================================================

  Widget _buildDesktopGameLayout() {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // --------------------------------------------------------
        // LEFT STATS PANEL
        // --------------------------------------------------------

        SizedBox(
          width: 190,
          child: _buildStats(),
        ),

        const SizedBox(width: 26),

        // --------------------------------------------------------
        // BOARD
        // --------------------------------------------------------

        Expanded(
          child: _buildBoard(),
        ),
      ],
    );
  }

  // ============================================================
  // MOBILE GAME LAYOUT
  // ============================================================

  Widget _buildMobileGameLayout() {
    return Column(
      children: [
        _buildMobileStats(),

        const SizedBox(height: 10),

        Expanded(
          child: _buildBoard(),
        ),
      ],
    );
  }

  // ============================================================
  // TOP BAR
  // ============================================================

  Widget _buildTopBar() {
    return Row(
      children: [
        Row(
          children: [
            Container(
              width: 46,
              height: 46,
              decoration: BoxDecoration(
                color: Theme.of(context)
                    .colorScheme
                    .primary
                    .withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(
                Icons.sailing_rounded,
                color: Theme.of(context).colorScheme.primary,
                size: 24,
              ),
            ),
            const SizedBox(width: 11),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'GRAND LINE',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 2,
                    color: Theme.of(context)
                        .colorScheme
                        .primary,
                  ),
                ),
                Text(
                  'MEMORY CHALLENGE',
                  style: TextStyle(
                    fontSize: 9,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.5,
                    color: Theme.of(context)
                        .colorScheme
                        .onSurface
                        .withValues(alpha: 0.55),
                  ),
                ),
              ],
            ),
          ],
        ),

        const Spacer(),

        Container(
          decoration: BoxDecoration(
            color: Theme.of(context)
                .colorScheme
                .surfaceContainerHighest
                .withValues(alpha: 0.6),
            borderRadius: BorderRadius.circular(14),
          ),
          child: IconButton(
            tooltip: 'Toggle theme',
            onPressed: widget.onToggleTheme,
            icon: Icon(
              widget.isDarkMode
                  ? Icons.light_mode_rounded
                  : Icons.dark_mode_rounded,
            ),
          ),
        ),
      ],
    );
  }

  // ============================================================
  // HERO
  // ============================================================

  Widget _buildHero() {
    return Column(
      children: [
        Text(
          'ONE PIECE',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.w900,
            letterSpacing: 4,
            height: 1,
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          'MEMORY MATCHER',
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w800,
            letterSpacing: 4,
            color: Theme.of(context)
                .colorScheme
                .onSurface
                .withValues(alpha: 0.65),
          ),
        ),
        const SizedBox(height: 5),
        Text(
          'Find all matching pirate crews',
          style: TextStyle(
            fontSize: 11,
            color: Theme.of(context)
                .colorScheme
                .onSurface
                .withValues(alpha: 0.5),
          ),
        ),
      ],
    );
  }

  // ============================================================
  // DESKTOP STATS
  // ============================================================

  Widget _buildStats() {
    return Column(
      children: [
        Expanded(
          child: _statCard(
            Icons.timer_outlined,
            'TIME',
            _formatTime(_seconds),
          ),
        ),

        const SizedBox(height: 10),

        Expanded(
          child: _statCard(
            Icons.touch_app_rounded,
            'MOVES',
            '$_moves',
          ),
        ),

        const SizedBox(height: 10),

        Expanded(
          child: _statCard(
            Icons.stars_rounded,
            'SCORE',
            '$_score',
          ),
        ),

        const SizedBox(height: 10),

        Expanded(
          child: _statCard(
            Icons.emoji_events_rounded,
            'BEST',
            '$_bestScore',
          ),
        ),
      ],
    );
  }

  // ============================================================
  // MOBILE STATS
  // ============================================================

  Widget _buildMobileStats() {
    return Row(
      children: [
        Expanded(
          child: _statCard(
            Icons.timer_outlined,
            'TIME',
            _formatTime(_seconds),
          ),
        ),

        const SizedBox(width: 7),

        Expanded(
          child: _statCard(
            Icons.touch_app_rounded,
            'MOVES',
            '$_moves',
          ),
        ),

        const SizedBox(width: 7),

        Expanded(
          child: _statCard(
            Icons.stars_rounded,
            'SCORE',
            '$_score',
          ),
        ),

        const SizedBox(width: 7),

        Expanded(
          child: _statCard(
            Icons.emoji_events_rounded,
            'BEST',
            '$_bestScore',
          ),
        ),
      ],
    );
  }

  // ============================================================
  // STAT CARD
  // ============================================================

  Widget _statCard(
    IconData icon,
    String label,
    String value,
  ) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
        horizontal: 15,
        vertical: 12,
      ),
      decoration: BoxDecoration(
        color: Theme.of(context)
            .colorScheme
            .surfaceContainerHighest
            .withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: Theme.of(context)
              .colorScheme
              .outline
              .withValues(alpha: 0.12),
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 38,
            height: 38,
            decoration: BoxDecoration(
              color: Theme.of(context)
                  .colorScheme
                  .primary
                  .withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(11),
            ),
            child: Icon(
              icon,
              size: 20,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),

          const SizedBox(width: 11),

          Expanded(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 9,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 1.3,
                    color: Theme.of(context)
                        .colorScheme
                        .onSurface
                        .withValues(alpha: 0.55),
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ============================================================
  // BOARD
  // ============================================================

  Widget _buildBoard() {
    return LayoutBuilder(
      builder: (context, constraints) {
        const spacing = 12.0;
        const columns = 4;
        const rows = 4;

        final availableWidth =
            constraints.maxWidth -
            (spacing * (columns - 1));

        final availableHeight =
            constraints.maxHeight -
            (spacing * (rows - 1));

        final cardSize = min(
          availableWidth / columns,
          availableHeight / rows,
        );

        final boardWidth =
            (cardSize * columns) +
            (spacing * (columns - 1));

        final boardHeight =
            (cardSize * rows) +
            (spacing * (rows - 1));

        return Center(
          child: SizedBox(
            width: boardWidth,
            height: boardHeight,
            child: GridView.builder(
              padding: EdgeInsets.zero,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _cards.length,
              gridDelegate:
                  const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
                crossAxisSpacing: spacing,
                mainAxisSpacing: spacing,
                childAspectRatio: 1,
              ),
              itemBuilder: (context, index) {
                return _buildCard(index);
              },
            ),
          ),
        );
      },
    );
  }

  // ============================================================
  // CARD
  // ============================================================

  Widget _buildCard(int index) {
    final card = _cards[index];

    final visible =
        card.isFaceUp || card.isMatched;

    return GestureDetector(
      onTap: () => _handleCardTap(index),
      child: AnimatedScale(
        scale: card.isMatched ? 0.94 : 1.0,
        duration: const Duration(
          milliseconds: 180,
        ),
        child: AnimatedContainer(
          duration: const Duration(
            milliseconds: 180,
          ),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(15),
            boxShadow: [
              BoxShadow(
                blurRadius: visible ? 8 : 5,
                offset: const Offset(0, 3),
                color: Colors.black.withValues(
                  alpha: 0.25,
                ),
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(15),
            child: AnimatedSwitcher(
              duration: const Duration(
                milliseconds: 220,
              ),
              transitionBuilder: (
                child,
                animation,
              ) {
                return FadeTransition(
                  opacity: animation,
                  child: ScaleTransition(
                    scale: animation,
                    child: child,
                  ),
                );
              },
              child: visible
                  ? _buildCardFront(card)
                  : _buildCardBack(),
            ),
          ),
        ),
      ),
    );
  }

  // ============================================================
  // CARD BACK
  // ============================================================

  Widget _buildCardBack() {
    return Container(
      key: const ValueKey('back'),
      decoration: BoxDecoration(
        color: Theme.of(context)
            .colorScheme
            .surface,
        borderRadius: BorderRadius.circular(15),
      ),
      child: Image.asset(
        'assets/cards/card_back.png',
        fit: BoxFit.cover,
        errorBuilder: (
          context,
          error,
          stackTrace,
        ) {
          return Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Theme.of(context)
                      .colorScheme
                      .primary,
                  Theme.of(context)
                      .colorScheme
                      .primary
                      .withValues(alpha: 0.65),
                ],
              ),
            ),
            child: const Center(
              child: Text(
                '☠',
                style: TextStyle(
                  fontSize: 40,
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  // ============================================================
  // CARD FRONT
  // ============================================================

  Widget _buildCardFront(
    MemoryCard card,
  ) {
    return Container(
      key: ValueKey(card.character),
      decoration: BoxDecoration(
        color: Theme.of(context)
            .colorScheme
            .surfaceContainerHighest,
        border: Border.all(
          color: card.isMatched
              ? Theme.of(context)
                  .colorScheme
                  .primary
              : Theme.of(context)
                  .colorScheme
                  .outline
                  .withValues(alpha: 0.15),
          width: card.isMatched ? 3 : 1,
        ),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Padding(
            padding: const EdgeInsets.all(3),
            child: Image.asset(
              'assets/cards/${card.character}.png',
              fit: BoxFit.cover,
              errorBuilder: (
                context,
                error,
                stackTrace,
              ) {
                return Center(
                  child: Text(
                    card.character.toUpperCase(),
                    style: const TextStyle(
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                );
              },
            ),
          ),

          // ------------------------------------------------------
          // MATCHED CHECK
          // ------------------------------------------------------

          if (card.isMatched)
            Positioned(
              top: 7,
              right: 7,
              child: Container(
                width: 25,
                height: 25,
                decoration: BoxDecoration(
                  color: Colors.green.shade600,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check_rounded,
                  size: 17,
                  color: Colors.white,
                ),
              ),
            ),
        ],
      ),
    );
  }

  // ============================================================
  // NEW GAME BUTTON
  // ============================================================

  Widget _buildNewGameButton({
    bool compact = false,
  }) {
    return SizedBox(
      width: 300,
      height: compact ? 42 : 48,
      child: FilledButton.icon(
        onPressed: _startNewGame,
        icon: const Icon(
          Icons.refresh_rounded,
          size: 20,
        ),
        label: const Text(
          'NEW GAME',
          style: TextStyle(
            fontWeight: FontWeight.w900,
            letterSpacing: 1.5,
          ),
        ),
        style: FilledButton.styleFrom(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
        ),
      ),
    );
  }
}