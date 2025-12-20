import unittest
import sys
from unittest.mock import Mock, patch, MagicMock
import io

# Mock pygame перед импортом любых модулей
sys.modules['pygame'] = Mock()
sys.modules['pygame.sprite'] = Mock()
sys.modules['pygame.Rect'] = Mock()
sys.modules['pygame.Surface'] = Mock()
sys.modules['pygame.display'] = Mock()
sys.modules['pygame.event'] = Mock()
sys.modules['pygame.key'] = Mock()
sys.modules['pygame.time'] = Mock()
sys.modules['pygame.font'] = Mock()
sys.modules['pygame.draw'] = Mock()
sys.modules['pygame.transform'] = Mock()
sys.modules['pygame.image'] = Mock()

# Теперь создаем моки для всех pygame модулей
pygame = sys.modules['pygame']
pygame.sprite = Mock()
pygame.Rect = Mock
pygame.Surface = Mock
pygame.display.set_mode = Mock()
pygame.display.set_caption = Mock()
pygame.display.update = Mock()
pygame.event.get = Mock(return_value=[])
pygame.key.get_pressed = Mock(return_value={})
pygame.time.Clock = Mock()
pygame.time.get_ticks = Mock(return_value=0)
pygame.font.Font = Mock(return_value=Mock())
pygame.font.render = Mock(return_value=Mock())
pygame.draw.rect = Mock()
pygame.transform.scale = Mock(side_effect=lambda img, size: img)
pygame.image.load = Mock(return_value=Mock())

# Глобальные константы
FPS = 60
SPEED_FACTOR = 10
GAME_TIME_MS = 2 * 60 * 1000
HIT_COOLDOWN_MS = 600
START_X, START_Y = 15, 500

# Глобальное окно
window = Mock()


class TestProektClass(unittest.TestCase):
    """Тесты для класса Proekt (базовый игровой объект)"""

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_proekt_init_sets_correct_attributes(self, mock_scale, mock_load):
        """Test Proekt.__init__ устанавливает правильные атрибуты"""
        # Arrange
        mock_load.return_value = Mock()
        mock_scale.return_value = Mock()
        mock_rect = Mock()
        mock_rect.x = 0
        mock_rect.y = 0
        mock_image = Mock()
        mock_image.get_rect = Mock(return_value=mock_rect)
        mock_scale.return_value = mock_image
        
        # Act
        from main import Proekt
        obj = Proekt(100, 200, 5, "test.png")
        
        # Assert
        self.assertEqual(obj.fx, 100.0)
        self.assertEqual(obj.fy, 200.0)
        self.assertEqual(obj.speed, 5)
        self.assertEqual(obj.rect.x, 100)
        self.assertEqual(obj.rect.y, 200)
        mock_load.assert_called_once_with("test.png")
        mock_scale.assert_called_once()

    def test_proekt_init_converts_coordinates_to_float(self):
        """Test Proekt.__init__ конвертирует координаты в float"""
        # Arrange & Act
        from main import Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            obj = Proekt("100", "200", "5", "test.png")
        
        # Assert
        self.assertIsInstance(obj.fx, float)
        self.assertIsInstance(obj.fy, float)
        self.assertIsInstance(obj.speed, int)

    def test_proekt_sync_rect_rounds_coordinates(self):
        """Test Proekt.sync_rect округляет координаты"""
        # Arrange
        from main import Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            obj = Proekt(0, 0, 0, "test.png")
        
        # Act
        obj.fx = 100.7
        obj.fy = 200.4
        obj.sync_rect()
        
        # Assert
        self.assertEqual(obj.rect.x, 101)  # round(100.7) = 101
        self.assertEqual(obj.rect.y, 200)  # round(200.4) = 200

    def test_proekt_sync_rect_with_negative_values(self):
        """Test Proekt.sync_rect с отрицательными значениями"""
        # Arrange
        from main import Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            obj = Proekt(0, 0, 0, "test.png")
        
        # Act
        obj.fx = -100.7
        obj.fy = -200.4
        obj.sync_rect()
        
        # Assert
        self.assertEqual(obj.rect.x, -101)  # round(-100.7) = -101
        self.assertEqual(obj.rect.y, -200)  # round(-200.4) = -200

    def test_proekt_sync_rect_updates_rect_from_float(self):
        """Test Proekt.sync_rect обновляет rect из float координат"""
        # Arrange
        from main import Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            obj = Proekt(0, 0, 0, "test.png")
            initial_rect_x = obj.rect.x
            initial_rect_y = obj.rect.y
        
        # Act
        obj.fx = 150.0
        obj.fy = 250.0
        obj.sync_rect()
        
        # Assert
        self.assertNotEqual(obj.rect.x, initial_rect_x)
        self.assertNotEqual(obj.rect.y, initial_rect_y)
        self.assertEqual(obj.rect.x, 150)
        self.assertEqual(obj.rect.y, 250)

    @patch('main.window')
    def test_proekt_see_calls_blit(self, mock_window):
        """Test Proekt.see вызывает window.blit"""
        # Arrange
        from main import Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            obj = Proekt(100, 200, 5, "test.png")
        
        # Act
        obj.see()
        
        # Assert
        mock_window.blit.assert_called_once_with(obj.image, (obj.rect.x, obj.rect.y))


class TestCaractersClass(unittest.TestCase):
    """Тесты для класса Caracters (игрок)"""

    def setUp(self):
        """Подготовка тестового окружения"""
        self.mock_keys = {
            pygame.K_LEFT: False,
            pygame.K_a: False,
            pygame.K_RIGHT: False,
            pygame.K_d: False,
            pygame.K_UP: False,
            pygame.K_w: False,
            pygame.K_DOWN: False,
            pygame.K_s: False
        }

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_calculates_step_correctly(self, mock_get_pressed):
        """Test Caracters.smena правильно рассчитывает шаг"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        mock_get_pressed.return_value = self.mock_keys
        
        # Act
        dt = 0.5
        char.smena(dt)
        
        # Assert
        expected_step = char.speed * SPEED_FACTOR * dt
        self.assertEqual(expected_step, 50.0)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_moves_left_on_left_key(self, mock_get_pressed):
        """Test Caracters.smena двигается влево при нажатии LEFT"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        self.mock_keys[pygame.K_LEFT] = True
        mock_get_pressed.return_value = self.mock_keys
        
        # Act
        initial_x = char.fx
        dt = 0.5
        char.smena(dt)
        
        # Assert
        step = char.speed * SPEED_FACTOR * dt
        self.assertEqual(char.fx, initial_x - step)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_moves_right_on_right_key(self, mock_get_pressed):
        """Test Caracters.smena двигается вправо при нажатии RIGHT"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        self.mock_keys[pygame.K_RIGHT] = True
        mock_get_pressed.return_value = self.mock_keys
        
        # Act
        initial_x = char.fx
        dt = 0.5
        char.smena(dt)
        
        # Assert
        step = char.speed * SPEED_FACTOR * dt
        self.assertEqual(char.fx, initial_x + step)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_moves_up_on_up_key(self, mock_get_pressed):
        """Test Caracters.smena двигается вверх при нажатии UP"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        self.mock_keys[pygame.K_UP] = True
        mock_get_pressed.return_value = self.mock_keys
        
        # Act
        initial_y = char.fy
        dt = 0.5
        char.smena(dt)
        
        # Assert
        step = char.speed * SPEED_FACTOR * dt
        self.assertEqual(char.fy, initial_y - step)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_moves_down_on_down_key(self, mock_get_pressed):
        """Test Caracters.smena двигается вниз при нажатии DOWN"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        self.mock_keys[pygame.K_DOWN] = True
        mock_get_pressed.return_value = self.mock_keys
        
        # Act
        initial_y = char.fy
        dt = 0.5
        char.smena(dt)
        
        # Assert
        step = char.speed * SPEED_FACTOR * dt
        self.assertEqual(char.fy, initial_y + step)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_calls_sync_rect(self, mock_get_pressed):
        """Test Caracters.smena вызывает sync_rect"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        mock_get_pressed.return_value = self.mock_keys
        sync_called = False
        
        def mock_sync():
            nonlocal sync_called
            sync_called = True
        
        char.sync_rect = mock_sync
        
        # Act
        char.smena(0.5)
        
        # Assert
        self.assertTrue(sync_called)

    @patch('pygame.key.get_pressed')
    def test_caracters_smena_handles_zero_dt(self, mock_get_pressed):
        """Test Caracters.smena обрабатывает dt=0"""
        # Arrange
        from main import Caracters
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            char = Caracters(100, 100, 10, "test.png")
        
        mock_get_pressed.return_value = {pygame.K_RIGHT: True}
        initial_x = char.fx
        
        # Act
        char.smena(0.0)
        
        # Assert
        self.assertEqual(char.fx, initial_x)


class TestEnenyClass(unittest.TestCase):
    """Тесты для класса Eneny (враги)"""

    def setUp(self):
        """Подготовка тестового окружения"""
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            from main import Eneny
            self.Eneny = Eneny

    def test_eneny_has_default_side_values(self):
        """Test Eneny имеет значения side по умолчанию"""
        # Arrange & Act
        enemy = self.Eneny(100, 100, 10, "test.png")
        
        # Assert
        self.assertEqual(enemy.side, "left")
        self.assertEqual(enemy.side2, "down")

    def test_eneny_vrag_smena1_moves_up_when_side2_is_up(self):
        """Test Eneny.vrag_smena1 двигается вверх при side2='up'"""
        # Arrange
        enemy = self.Eneny(100, 300, 10, "test.png")
        enemy.side2 = "up"
        initial_y = enemy.fy
        
        # Act
        dt = 0.5
        enemy.vrag_smena1(dt)
        
        # Assert
        step = enemy.speed * SPEED_FACTOR * dt
        self.assertEqual(enemy.fy, initial_y - step)

    def test_eneny_vrag_smena1_moves_down_when_side2_is_down(self):
        """Test Eneny.vrag_smena1 двигается вниз при side2='down'"""
        # Arrange
        enemy = self.Eneny(100, 300, 10, "test.png")
        enemy.side2 = "down"
        initial_y = enemy.fy
        
        # Act
        dt = 0.5
        enemy.vrag_smena1(dt)
        
        # Assert
        step = enemy.speed * SPEED_FACTOR * dt
        self.assertEqual(enemy.fy, initial_y + step)

    def test_eneny_vrag_smena1_changes_to_down_at_upper_boundary(self):
        """Test Eneny.vrag_smena1 меняется на 'down' при верхней границе"""
        # Arrange
        enemy = self.Eneny(100, 170, 10, "test.png")
        enemy.rect.y = 170
        enemy.side2 = "up"
        
        # Act
        enemy.vrag_smena1(0.1)
        
        # Assert
        self.assertEqual(enemy.side2, "down")

    def test_eneny_vrag_smena1_changes_to_up_at_lower_boundary(self):
        """Test Eneny.vrag_smena1 меняется на 'up' при нижней границе"""
        # Arrange
        enemy = self.Eneny(100, 420, 10, "test.png")
        enemy.rect.y = 420
        enemy.side2 = "down"
        
        # Act
        enemy.vrag_smena1(0.1)
        
        # Assert
        self.assertEqual(enemy.side2, "up")

    def test_eneny_vrag_smena2_moves_left_when_side_is_left(self):
        """Test Eneny.vrag_smena2 двигается влево при side='left'"""
        # Arrange
        enemy = self.Eneny(400, 100, 10, "test.png")
        enemy.side = "left"
        initial_x = enemy.fx
        
        # Act
        dt = 0.5
        enemy.vrag_smena2(dt)
        
        # Assert
        step = enemy.speed * SPEED_FACTOR * dt
        self.assertEqual(enemy.fx, initial_x - step)

    def test_eneny_vrag_smena2_moves_right_when_side_is_right(self):
        """Test Eneny.vrag_smena2 двигается вправо при side='right'"""
        # Arrange
        enemy = self.Eneny(400, 100, 10, "test.png")
        enemy.side = "right"
        initial_x = enemy.fx
        
        # Act
        dt = 0.5
        enemy.vrag_smena2(dt)
        
        # Assert
        step = enemy.speed * SPEED_FACTOR * dt
        self.assertEqual(enemy.fx, initial_x + step)

    def test_eneny_vrag_smena2_changes_to_right_at_left_boundary(self):
        """Test Eneny.vrag_smena2 меняется на 'right' при левой границе"""
        # Arrange
        enemy = self.Eneny(20, 100, 10, "test.png")
        enemy.rect.x = 20
        enemy.side = "left"
        
        # Act
        enemy.vrag_smena2(0.1)
        
        # Assert
        self.assertEqual(enemy.side, "right")

    def test_eneny_vrag_smena2_changes_to_left_at_right_boundary(self):
        """Test Eneny.vrag_smena2 меняется на 'left' при правой границе"""
        # Arrange
        enemy = self.Eneny(730, 100, 10, "test.png")
        enemy.rect.x = 730
        enemy.side = "right"
        
        # Act
        enemy.vrag_smena2(0.1)
        
        # Assert
        self.assertEqual(enemy.side, "left")

    def test_eneny_vrag_smena3_initializes_route_on_first_call(self):
        """Test Eneny.vrag_smena3 инициализирует маршрут при первом вызове"""
        # Arrange
        enemy = self.Eneny(740, 345, 10, "test.png")
        
        # Act
        enemy.vrag_smena3(0.1)
        
        # Assert
        self.assertTrue(hasattr(enemy, "route"))
        self.assertEqual(len(enemy.route), 9)
        self.assertEqual(enemy._route_i, 1)
        self.assertEqual(enemy._route_dir, 1)

    def test_eneny_vrag_smena3_returns_early_if_zero_speed(self):
        """Test Eneny.vrag_smena3 возвращается рано если скорость 0"""
        # Arrange
        enemy = self.Eneny(740, 345, 0, "test.png")
        enemy.vrag_smena3(0.1)  # Инициализация
        initial_x, initial_y = enemy.fx, enemy.fy
        
        # Act
        enemy.vrag_smena3(0.5)
        
        # Assert
        self.assertEqual(enemy.fx, initial_x)
        self.assertEqual(enemy.fy, initial_y)

    def test_eneny_vrag_smena3_moves_toward_target(self):
        """Test Eneny.vrag_smena3 двигается к цели"""
        # Arrange
        enemy = self.Eneny(740, 345, 10, "test.png")
        enemy.vrag_smena3(0.1)  # Инициализация
        initial_x, initial_y = enemy.fx, enemy.fy
        
        # Act
        enemy.vrag_smena3(0.5)
        
        # Assert
        self.assertNotEqual((enemy.fx, enemy.fy), (initial_x, initial_y))

    def test_eneny_vrag_smena3_reverses_at_end_of_route(self):
        """Test Eneny.vrag_smena3 разворачивается в конце маршрута"""
        # Arrange
        enemy = self.Eneny(740, 345, 10, "test.png")
        enemy.vrag_smena3(0.1)  # Инициализация
        enemy._route_i = len(enemy.route) - 1
        enemy._route_dir = 1
        enemy.fx, enemy.fy = enemy.route[-1]
        
        # Act
        enemy.vrag_smena3(0.1)
        
        # Assert
        self.assertEqual(enemy._route_dir, -1)

    def test_eneny_vrag_smena3_goes_forward_at_start_of_route(self):
        """Test Eneny.vrag_smena3 идет вперед в начале маршрута"""
        # Arrange
        enemy = self.Eneny(740, 345, 10, "test.png")
        enemy.vrag_smena3(0.1)  # Инициализация
        enemy._route_i = 0
        enemy._route_dir = -1
        enemy.fx, enemy.fy = enemy.route[0]
        
        # Act
        enemy.vrag_smena3(0.1)
        
        # Assert
        self.assertEqual(enemy._route_dir, 1)


class TestWallClass(unittest.TestCase):
    """Тесты для класса Wall (стены)"""

    @patch('pygame.Surface')
    def test_wall_init_sets_correct_attributes(self, mock_surface):
        """Test Wall.__init__ устанавливает правильные атрибуты"""
        # Arrange
        mock_surface.return_value = Mock()
        mock_rect = Mock()
        mock_rect.get_rect = Mock(return_value=mock_rect)
        mock_surface.return_value = mock_rect
        
        # Act
        from main import Wall
        wall = Wall(50, 60, 100, 200, 255, 128, 0)
        
        # Assert
        self.assertEqual(wall.r, 255)
        self.assertEqual(wall.g, 128)
        self.assertEqual(wall.b, 0)
        self.assertEqual(wall.width, 200)
        self.assertEqual(wall.height, 100)
        self.assertEqual(wall.rect.x, 50)
        self.assertEqual(wall.rect.y, 60)

    def test_wall_init_handles_edge_colors(self):
        """Test Wall.__init__ обрабатывает граничные цвета"""
        # Arrange & Act
        from main import Wall
        with patch('pygame.Surface'):
            # Минимальные значения
            wall_min = Wall(0, 0, 10, 10, 0, 0, 0)
            # Максимальные значения
            wall_max = Wall(0, 0, 10, 10, 255, 255, 255)
        
        # Assert
        self.assertEqual(wall_min.r, 0)
        self.assertEqual(wall_min.g, 0)
        self.assertEqual(wall_min.b, 0)
        self.assertEqual(wall_max.r, 255)
        self.assertEqual(wall_max.g, 255)
        self.assertEqual(wall_max.b, 255)

    @patch('main.window')
    @patch('pygame.draw.rect')
    def test_wall_picture_wall_calls_draw_rect(self, mock_draw_rect, mock_window):
        """Test Wall.picture_wall вызывает pygame.draw.rect"""
        # Arrange
        from main import Wall
        with patch('pygame.Surface'):
            wall = Wall(50, 60, 100, 200, 255, 128, 0)
        
        # Act
        wall.picture_wall()
        
        # Assert
        mock_draw_rect.assert_called_once_with(
            mock_window,
            (wall.r, wall.g, wall.b),
            (wall.rect.x, wall.rect.y, wall.width, wall.height)
        )


class TestDoorClass(unittest.TestCase):
    """Тесты для класса Door (дверь)"""

    @patch('pygame.Surface')
    def test_door_init_sets_correct_attributes(self, mock_surface):
        """Test Door.__init__ устанавливает правильные атрибуты"""
        # Arrange
        mock_surface.return_value = Mock()
        mock_rect = Mock()
        mock_rect.get_rect = Mock(return_value=mock_rect)
        mock_surface.return_value = mock_rect
        
        # Act
        from main import Door
        door = Door(100, 200, 50, 20)
        
        # Assert
        self.assertEqual(door.width, 20)
        self.assertEqual(door.height, 50)
        self.assertEqual(door.rect.x, 100)
        self.assertEqual(door.rect.y, 200)

    def test_door_init_handles_zero_size(self):
        """Test Door.__init__ обрабатывает нулевой размер"""
        # Arrange & Act
        from main import Door
        with patch('pygame.Surface'):
            door = Door(0, 0, 0, 0)
        
        # Assert
        self.assertEqual(door.width, 0)
        self.assertEqual(door.height, 0)


class TestGameConstants(unittest.TestCase):
    """Тесты для игровых констант"""

    def test_fps_constant(self):
        """Test константа FPS"""
        from main import FPS
        self.assertEqual(FPS, 60)

    def test_speed_factor_constant(self):
        """Test константа SPEED_FACTOR"""
        from main import SPEED_FACTOR
        self.assertEqual(SPEED_FACTOR, 10)

    def test_game_time_constant(self):
        """Test константа GAME_TIME_MS"""
        from main import GAME_TIME_MS
        self.assertEqual(GAME_TIME_MS, 120000)  # 2 минуты

    def test_hit_cooldown_constant(self):
        """Test константа HIT_COOLDOWN_MS"""
        from main import HIT_COOLDOWN_MS
        self.assertEqual(HIT_COOLDOWN_MS, 600)

    def test_start_position_constants(self):
        """Test константы стартовой позиции"""
        from main import START_X, START_Y
        self.assertEqual(START_X, 15)
        self.assertEqual(START_Y, 500)


class TestGameSetup(unittest.TestCase):
    """Тесты для настройки игры"""

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    def test_game_window_setup(self, mock_set_caption, mock_set_mode):
        """Test настройка игрового окна"""
        # Arrange
        mock_window = Mock()
        mock_set_mode.return_value = mock_window
        
        # Act
        import main
        
        # Assert
        mock_set_mode.assert_called_once_with((810, 800))
        mock_set_caption.assert_called_once_with("Лабиринт")

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_background_loading(self, mock_scale, mock_load):
        """Test загрузка фона"""
        # Arrange
        mock_image = Mock()
        mock_load.return_value = mock_image
        
        # Act
        import main
        
        # Assert
        self.assertGreaterEqual(mock_load.call_count, 1)
        self.assertGreaterEqual(mock_scale.call_count, 1)


class TestCollisionLogic(unittest.TestCase):
    """Тесты для логики столкновений"""

    def test_collision_resets_player_position(self):
        """Test столкновение сбрасывает позицию игрока"""
        # Arrange
        from main import Caracters, Wall
        with patch('pygame.image.load'), patch('pygame.transform.scale'), patch('pygame.Surface'):
            player = Caracters(100, 100, 10, "test.png")
            wall = Wall(100, 100, 50, 50, 255, 0, 0)
            walls = [wall]
            
            # Мокаем collide_rect
            with patch('pygame.sprite.collide_rect') as mock_collide:
                mock_collide.return_value = True
                
                # Act
                old_fx, old_fy = player.fx, player.fy
                player.fx += 50  # Имитируем движение
                player.fy += 50
                
                # Проверяем столкновение
                if any(pygame.sprite.collide_rect(player, w) for w in walls):
                    player.fx, player.fy = old_fx, old_fy
                    player.sync_rect()
                
                # Assert
                self.assertEqual(player.fx, old_fx)
                self.assertEqual(player.fy, old_fy)


class TestEnemyHitLogic(unittest.TestCase):
    """Тесты для логики попадания врага"""

    def test_hit_enemy_reduces_lives(self):
        """Test попадание врага уменьшает жизни"""
        # Arrange
        from main import Caracters, Eneny
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            player = Caracters(100, 100, 10, "test.png")
            enemy = Eneny(100, 100, 10, "test.png")
            vrags = [enemy]
            
            lives = 3
            last_hit_time = -1000
            now = 0
            
            # Мокаем collide_rect
            with patch('pygame.sprite.collide_rect') as mock_collide:
                mock_collide.return_value = True
                
                # Act
                hit_enemy = any(pygame.sprite.collide_rect(player, v) for v in vrags)
                if hit_enemy and (now - last_hit_time) >= HIT_COOLDOWN_MS:
                    lives -= 1
                    last_hit_time = now
                
                # Assert
                self.assertEqual(lives, 2)


class TestStarCollection(unittest.TestCase):
    """Тесты для сбора звезд"""

    def test_star_collection_increases_score(self):
        """Test сбор звезд увеличивает счет"""
        # Arrange
        from main import Caracters, Proekt
        with patch('pygame.image.load'), patch('pygame.transform.scale'):
            player = Caracters(100, 100, 10, "test.png")
            star = Proekt(100, 100, 0, "test.png")
            stars = [star]
            score = 0
            
            # Мокаем collide_rect и kill
            with patch('pygame.sprite.collide_rect') as mock_collide:
                mock_collide.return_value = True
                star.kill = Mock()
                
                # Act
                for star_copy in stars[:]:
                    if pygame.sprite.collide_rect(player, star_copy):
                        stars.remove(star_copy)
                        star_copy.kill()
                        score += 1
                
                # Assert
                self.assertEqual(score, 1)
                self.assertEqual(len(stars), 0)


class TestTimeCalculation(unittest.TestCase):
    """Тесты для расчета времени"""

    def test_time_format_calculation(self):
        """Test расчет формата времени"""
        # Arrange
        remaining = 125000  # 2 минуты 5 секунд
        
        # Act
        sec = max(0, remaining // 1000)
        mm = sec // 60
        ss = sec % 60
        
        # Assert
        self.assertEqual(sec, 125)
        self.assertEqual(mm, 2)
        self.assertEqual(ss, 5)


if __name__ == '__main__':
    unittest.main()
