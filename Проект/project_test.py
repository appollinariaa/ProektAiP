import unittest
from unittest.mock import MagicMock, patch
import main  # Ваш файл с кодом

class TestProekt(unittest.TestCase):
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_proekt_init(self, mock_scale, mock_load):
        mock_surface = MagicMock()
        mock_load.return_value = mock_surface
        mock_scale.return_value = mock_surface
        # Создаем объект
        sprite = main.Proekt(10.5, 20.5, 5, 'path/to/image.png')
        self.assertEqual(sprite.fx, 10.5)
        self.assertEqual(sprite.fy, 20.5)
        self.assertEqual(sprite.rect.x, int(10.5))
        self.assertEqual(sprite.rect.y, int(20.5))
        self.assertEqual(sprite.image, mock_surface)
        self.assertEqual(sprite.speed, 5)

class TestCaracters(unittest.TestCase):
    @patch('pygame.key.get_pressed')
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_smena_moves_left_right_up_down(self, mock_scale, mock_load, mock_get_pressed):
        mock_surface = MagicMock()
        mock_load.return_value = mock_surface
        mock_scale.return_value = mock_surface
        sprite = main.Caracters(0, 0, 1, 'path/to/image.png')
        sprite.fx = 0
        sprite.fy = 0
        # Мокать нажатия клавиш
        mock_get_pressed.return_value = {
            main.K_LEFT: True,
            main.K_RIGHT: False,
            main.K_UP: False,
            main.K_DOWN: False,
            main.K_a: False,
            main.K_w: False,
            main.K_s: False,
            main.K_d: False
        }
        sprite.smena(0.1)
        self.assertLess(sprite.fx, 0)
        # Аналогично для других клавиш

class TestEneny(unittest.TestCase):
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_vrag_smena1_direction_changes(self, mock_scale, mock_load):
        mock_surface = MagicMock()
        mock_load.return_value = mock_surface
        mock_scale.return_value = mock_surface
        enemy = main.Eneny(200, 170, 1, 'path')
        enemy.side2 = "up"
        enemy.rect = MagicMock()
        enemy.rect.y = 170
        enemy.fy = 170
        enemy.vrag_smena1(0.1)
        self.assertIn(enemy.side2, ["up", "down"])

    # Аналогично тесты для vrag_smena2, vrag_smena3

class TestWall(unittest.TestCase):
    @patch('pygame.Surface')
    def test_picture_wall_calls_draw_rect(self, mock_surface):
        mock_surface.return_value = MagicMock()
        wall = main.Wall(10, 20, 30, 40, 100, 150, 200)
        with patch('pygame.draw.rect') as mock_rect:
            wall.picture_wall()
            mock_rect.assert_called_once()

class TestDoor(unittest.TestCase):
    def test_init(self):
        door = main.Door(10, 20, 30, 40)
        self.assertEqual(door.rect.x, 10)
        self.assertEqual(door.rect.y, 20)

# Можно добавить тесты для логики столкновений, подсчета времени и т.п.,
# мокая pygame.time.get_ticks, sprite.collide_rect и т.д.

if __name__ == '__main__':
    unittest.main()
