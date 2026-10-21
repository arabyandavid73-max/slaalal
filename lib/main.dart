import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const OsintApp());
}

class OsintApp extends StatelessWidget {
  const OsintApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OSINT Search',
      theme: ThemeData.dark(useMaterial3: true),
      home: const SearchScreen(),
    );
  }
}

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});
  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _controller = TextEditingController();
  List<dynamic> _results = [];
  bool _loading = false;
  String _status = 'Введите запрос';

  Future<void> _search() async {
    if (_controller.text.trim().isEmpty) return;
    setState(() { _loading = true; _status = 'Ищу...'; });
    
    try {
      final res = await http.post(
        Uri.parse('http://127.0.0.1:5000/search'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'query': _controller.text.trim()}),
      ).timeout(const Duration(seconds: 60));
      
      final data = jsonDecode(res.body);
      setState(() {
        _results = data['results'];
        _status = 'Найдено: ${data['total']} за ${data['time']} сек';
        _loading = false;
      });
    } catch (e) {
      setState(() { _loading = false; _status = 'Ошибка: сервер не отвечает'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🕵 OSINT Search'),
        centerTitle: true,
        backgroundColor: const Color(0xFF1a1a2e),
      ),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(children: [
          TextField(
            controller: _controller,
            decoration: InputDecoration(
              hintText: 'ФИО, телефон, email...',
              suffixIcon: IconButton(
                icon: const Icon(Icons.search, color: Color(0xFF4ade80)),
                onPressed: _search,
              ),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onSubmitted: (_) => _search(),
          ),
          const SizedBox(height: 8),
          if (_loading) const LinearProgressIndicator(color: Color(0xFF4ade80)),
          Text(_status, style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 8),
          Expanded(
            child: ListView.builder(
              itemCount: _results.length,
              itemBuilder: (_, i) {
                final r = _results[i];
                return Card(
                  color: const Color(0xFF1a1a2e),
                  child: ListTile(
                    title: Text(r['line'], style: const TextStyle(fontSize: 13, color: Colors.white)),
                    subtitle: Text(r['base'], style: const TextStyle(color: Color(0xFF4ade80), fontSize: 11)),
                    trailing: IconButton(
                      icon: const Icon(Icons.copy, size: 18, color: Colors.grey),
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: r['line']));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Скопировано'), duration: Duration(seconds: 1)),
                        );
                      },
                    ),
                  ),
                );
              },
            ),
          ),
        ]),
      ),
    );
  }
}
