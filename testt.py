import unittest
import os
import tempfile
import shutil
import yaml
from main import GitVisualizer, load_config


class TestGitVisualizer(unittest.TestCase):
    def setUp(self):
        """
        Создает временную папку для вывода результатов и временный YAML файл конфигурации.
        """
        self.temp_dir = tempfile.mkdtemp()
        self.test_repo_url = "https://github.com/see12357/ConfigDZ-2.git"  # Пример публичного репозитория
        self.test_output_file = "test.puml"
        self.test_commit_date = "2024-11-15"
        self.config_path = os.path.join(self.temp_dir, "config.yaml")
        self.output_path = os.path.join(self.temp_dir, self.test_output_file)

        # Создание временного YAML-файла конфигурации
        config_data = {
            "repo_url": self.test_repo_url,
            "output_file": self.test_output_file,
            "commit_date": self.test_commit_date,
        }
        with open(self.config_path, 'w') as config_file:
            yaml.dump(config_data, config_file)

    def tearDown(self):
        """
        Удаляет временную папку и все её содержимое.
        """
        shutil.rmtree(self.temp_dir)

    def test_load_config(self):
        """
        Тестирует загрузку конфигурации из YAML.
        """
        config = load_config(self.config_path)
        self.assertEqual(config['repo_url'], self.test_repo_url)
        self.assertEqual(config['output_file'], self.test_output_file)
        self.assertEqual(config['commit_date'], self.test_commit_date)

    def test_clone_repository(self):
        """
        Тестирует клонирование репозитория.
        """
        config = load_config(self.config_path)
        visualizer = GitVisualizer(config)
        self.assertTrue(os.path.exists(visualizer.repo_path))
        self.assertTrue(os.path.isdir(visualizer.repo_path))

    def test_get_commits(self):
        """
        Тестирует получение списка коммитов.
        """
        config = load_config(self.config_path)
        visualizer = GitVisualizer(config)
        commits = visualizer.get_commits()
        self.assertIsInstance(commits, list)
        self.assertTrue(len(commits) > 0)
        self.assertIn('hash', commits[0])
        self.assertIn('message', commits[0])
        self.assertIn('files', commits[0])

    def test_build_graph(self):
        """
        Тестирует создание графа в формате PlantUML.
        """
        config = load_config(self.config_path)
        visualizer = GitVisualizer(config)
        commits = visualizer.get_commits()
        graph_content = visualizer.build_graph(commits)
        self.assertIsInstance(graph_content, str)
        self.assertTrue(graph_content.startswith("@startuml"))
        self.assertTrue(graph_content.endswith("@enduml"))

    def test_clone_repasitory(self):
        """
        Тестирует клонирование репозитория.
        """
        config = load_config(self.config_path)
        visualizer = GitVisualizer(config)
        self.assertTrue(os.path.exists(visualizer.repo_path))
        self.assertTrue(os.path.isdir(visualizer.repo_path))

if __name__ == "__main__":
    unittest.main()
