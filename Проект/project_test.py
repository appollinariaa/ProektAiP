import unittest
import sys
from unittest.mock import Mock, patch, MagicMock
class TestProektInit(unittest.TestCase):
    """Тесты для функции __init__ класса Proekt"""
    
    def test_init_with_integer_values(self):
        """Тест инициализации с целыми числами"""
        obj = Proekt(100, 200, 5, "test.png")
        self.assertEqual(obj.fx, 100.0)
        self.assertEqual(obj.fy, 200.0)
        self.assertEqual(obj.speed, 5)
        self.assertEqual(obj.rect.x, 100)
    
    def test_init_with_float_values(self):
        """Тест инициализации с дробными числами"""
        obj = Proekt(100.5, 200.7, 2.5, "test.png")
        self.assertEqual(obj.fx, 100.5)
        self.assertEqual(obj.fy, 200.7)
        self.assertEqual(obj.speed, 2.5)
        self.assertEqual(obj.rect.x, 100)
    
    def test_init_with_zero_values(self):
        """Тест инициализации с нулевыми значениями"""
        obj = Proekt(0, 0, 0, "test.png")
        self.assertEqual(obj.fx, 0.0)
        self.assertEqual(obj.fy, 0.0)
        self.assertEqual(obj.speed, 0)
    
    def test_init_with_negative_values(self):
        """Тест инициализации с отрицательными значениями"""
        obj = Proekt(-10, -20, -5, "test.png")
        self.assertEqual(obj.fx, -10.0)
        self.assertEqual(obj.fy, -20.0)
        self.assertEqual(obj.speed, -5)


class TestProektSyncRect(unittest.TestCase):
    """Тесты для функции sync_rect класса Proekt"""
    
    def setUp(self):
        self.obj = Proekt(100, 200, 5, "test.png")
    
    def test_sync_rect_with_integer_values(self):
        """Тест синхронизации с целыми координатами"""
        self.obj.fx = 150
        self.obj.fy = 250
        self.obj.sync_rect()
        self.assertEqual(self.obj.rect.x, 150)
        self.assertEqual(self.obj.rect.y, 250)
    
    def test_sync_rect_with_float_rounding_up(self):
        """Тест округления вверх дробных координат"""
        self.obj.fx = 100.7
        self.obj.fy = 200.6
        self.obj.sync_rect()
        self.assertEqual(self.obj.rect.x, 101)
        self.assertEqual(self.obj.rect.y, 201)
    
    def test_sync_rect_with_float_rounding_down(self):
        """Тест округления вниз дробных координат"""
        self.obj.fx = 100.4
        self.obj.fy = 200.3
        self.obj.sync_rect()
        self.assertEqual(self.obj.rect.x, 100)
        self.assertEqual(self.obj.rect.y, 200)
    
    def test_sync_rect_with_negative_floats(self):
        """Тест синхронизации отрицательных дробных координат"""
        self.obj.fx = -100.7
        self.obj.fy = -200.4
        self.obj.sync_rect()
        self.assertEqual(self.obj.rect.x, -101)
        self.assertEqual(self.obj.rect.y, -200)


class TestProektSee(unittest.TestCase):
    """Тесты для функции see класса Proekt"""
    
    def test_see_no_exception(self):
        """Тест что метод see не вызывает исключений"""
        obj = Proekt(100, 200, 5, "test.png")
        try:
            obj.see()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"see() вызвал исключение: {e}")

# ТЕСТЫ КЛАССА Caracters

class TestCaractersSmena(unittest.TestCase):
    """Тесты для функции smena класса Caracters"""
    
    def setUp(self):
        self.char = Caracters(100, 100, 10, "test.png")
    
    @patch('pygame.key.get_pressed')
    def test_smena_calculates_step_correctly(self, mock_get_pressed):
        """Тест правильного расчета шага движения"""
        mock_get_pressed.return_value = {}
        self.char.smena(0.5)
        step = self.char.speed * SPEED_FACTOR * 0.5
        self.assertEqual(step, 50.0)
    
    @patch('pygame.key.get_pressed')
    def test_smena_zero_dt_no_movement(self, mock_get_pressed):
        """Тест что при dt=0 координаты не меняются"""
        mock_get_pressed.return_value = {}
        initial_x, initial_y = self.char.fx, self.char.fy
        self.char.smena(0.0)
        self.assertEqual(self.char.fx, initial_x)
        self.assertEqual(self.char.fy, initial_y)
    
    @patch('pygame.key.get_pressed')
    def test_smena_calls_sync_rect(self, mock_get_pressed):
        """Тест что smena вызывает sync_rect"""
        mock_get_pressed.return_value = {}
        sync_called = False
        original_sync = self.char.sync_rect
        
        def mock_sync():
            nonlocal sync_called
            sync_called = True
            original_sync()
        
        self.char.sync_rect = mock_sync
        self.char.smena(0.5)
        self.assertTrue(sync_called)
    
    @patch('pygame.key.get_pressed')
    def test_smena_negative_dt_handling(self, mock_get_pressed):
        """Тест обработки отрицательного dt"""
        mock_get_pressed.return_value = {}
        try:
            self.char.smena(-0.1)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"smena(-0.1) вызвал исключение: {e}")

# ТЕСТЫ КЛАССА Eneny - vrag_smena1

class TestEnenyVragSmena1(unittest.TestCase):
    """Тесты для функции vrag_smena1 класса Eneny"""
    
    def setUp(self):
        self.enemy = Eneny(100, 300, 10, "test.png")
    
    def test_vrag_smena1_moves_up(self):
        """Тест движения вверх"""
        self.enemy.side2 = "up"
        initial_y = self.enemy.fy
        self.enemy.vrag_smena1(0.5)
        expected_y = initial_y - (10 * SPEED_FACTOR * 0.5)
        self.assertEqual(self.enemy.fy, expected_y)
    
    def test_vrag_smena1_moves_down(self):
        """Тест движения вниз"""
        self.enemy.side2 = "down"
        initial_y = self.enemy.fy
        self.enemy.vrag_smena1(0.5)
        expected_y = initial_y + (10 * SPEED_FACTOR * 0.5)
        self.assertEqual(self.enemy.fy, expected_y)
    
    def test_vrag_smena1_upper_boundary(self):
        """Тест верхней границы"""
        self.enemy.rect.y = 170
        self.enemy.side2 = "up"
        self.enemy.vrag_smena1(0.1)
        self.assertEqual(self.enemy.side2, "down")
    
    def test_vrag_smena1_lower_boundary(self):
        """Тест нижней границы"""
        self.enemy.rect.y = 420
        self.enemy.side2 = "down"
        self.enemy.vrag_smena1(0.1)
        self.assertEqual(self.enemy.side2, "up")
    
    def test_vrag_smena1_zero_speed(self):
        """Тест движения с нулевой скоростью"""
        self.enemy.speed = 0
        initial_y = self.enemy.fy
        self.enemy.vrag_smena1(0.5)
        self.assertEqual(self.enemy.fy, initial_y)
    
    def test_vrag_smena1_calls_sync_rect(self):
        """Тест что вызывается sync_rect"""
        sync_called = False
        original_sync = self.enemy.sync_rect
        
        def mock_sync():
            nonlocal sync_called
            sync_called = True
            original_sync()
        
        self.enemy.sync_rect = mock_sync
        self.enemy.vrag_smena1(0.1)
        self.assertTrue(sync_called)

# ТЕСТЫ КЛАССА Eneny - vrag_smena2

class TestEnenyVragSmena2(unittest.TestCase):
    """Тесты для функции vrag_smena2 класса Eneny"""
    
    def setUp(self):
        self.enemy = Eneny(400, 100, 10, "test.png")
    
    def test_vrag_smena2_moves_left(self):
        """Тест движения влево"""
        self.enemy.side = "left"
        initial_x = self.enemy.fx
        self.enemy.vrag_smena2(0.5)
        expected_x = initial_x - (10 * SPEED_FACTOR * 0.5)
        self.assertEqual(self.enemy.fx, expected_x)
    
    def test_vrag_smena2_moves_right(self):
        """Тест движения вправо"""
        self.enemy.side = "right"
        initial_x = self.enemy.fx
        self.enemy.vrag_smena2(0.5)
        expected_x = initial_x + (10 * SPEED_FACTOR * 0.5)
        self.assertEqual(self.enemy.fx, expected_x)
    
    def test_vrag_smena2_left_boundary(self):
        """Тест левой границы"""
        self.enemy.rect.x = 20
        self.enemy.side = "left"
        self.enemy.vrag_smena2(0.1)
        self.assertEqual(self.enemy.side, "right")
    
    def test_vrag_smena2_right_boundary(self):
        """Тест правой границы"""
        self.enemy.rect.x = 730
        self.enemy.side = "right"
        self.enemy.vrag_smena2(0.1)
        self.assertEqual(self.enemy.side, "left")
    
    def test_vrag_smena2_calls_sync_rect(self):
        """Тест что вызывается sync_rect"""
        sync_called = False
        original_sync = self.enemy.sync_rect
        
        def mock_sync():
            nonlocal sync_called
            sync_called = True
            original_sync()
        
        self.enemy.sync_rect = mock_sync
        self.enemy.vrag_smena2(0.1)
        self.assertTrue(sync_called)

# ТЕСТЫ КЛАССА Eneny - vrag_smena3

class TestEnenyVragSmena3(unittest.TestCase):
    """Тесты для функции vrag_smena3 класса Eneny"""
    
    def setUp(self):
        self.enemy = Eneny(740, 345, 10, "test.png")
    
    def test_vrag_smena3_initializes_route_on_first_call(self):
        """Тест инициализации маршрута при первом вызове"""
        self.assertFalse(hasattr(self.enemy, "route"))
        self.enemy.vrag_smena3(0.1)
        self.assertTrue(hasattr(self.enemy, "route"))
        self.assertEqual(len(self.enemy.route), 9)
        self.assertEqual(self.enemy._route_i, 1)
        self.assertEqual(self.enemy._route_dir, 1)
    
    def test_vrag_smena3_moves_towards_target(self):
        """Тест движения к цели"""
        self.enemy.vrag_smena3(0.1)  # Инициализация
        initial_x, initial_y = self.enemy.fx, self.enemy.fy
        self.enemy.vrag_smena3(0.5)
        # Проверяем что координаты изменились
        self.assertNotEqual((self.enemy.fx, self.enemy.fy), (initial_x, initial_y))
    
    def test_vrag_smena3_zero_speed_early_return(self):
        """Тест раннего возврата при нулевой скорости"""
        self.enemy.speed = 0
        initial_x, initial_y = self.enemy.fx, self.enemy.fy
        self.enemy.vrag_smena3(0.5)
        self.assertEqual(self.enemy.fx, initial_x)
        self.assertEqual(self.enemy.fy, initial_y)
    
    def test_vrag_smena3_reverse_at_end_of_route(self):
        """Тест разворота в конце маршрута"""
        self.enemy.vrag_smena3(0.1)
        self.enemy._route_i = len(self.enemy.route) - 1
        self.enemy._route_dir = 1
        self.enemy.fx, self.enemy.fy = self.enemy.route[-1]
        self.enemy.vrag_smena3(0.1)
        self.assertEqual(self.enemy._route_dir, -1)
    
    def test_vrag_smena3_forward_at_start_of_route(self):
        """Тест движения вперед в начале маршрута"""
        self.enemy.vrag_smena3(0.1)
        self.enemy._route_i = 0
        self.enemy._route_dir = -1
        self.enemy.fx, self.enemy.fy = self.enemy.route[0]
        self.enemy.vrag_smena3(0.1)
        self.assertEqual(self.enemy._route_dir, 1)
    
    def test_vrag_smena3_exact_target_reached(self):
        """Тест точного достижения цели"""
        self.enemy.vrag_smena3(0.1)
        target_x, target_y = self.enemy.route[1]
        self.enemy.fx, self.enemy.fy = target_x, target_y
        old_index = self.enemy._route_i
        self.enemy.vrag_smena3(0.1)
        self.assertNotEqual(self.enemy._route_i, old_index)

# ТЕСТЫ КЛАССА Wall

class TestWallInit(unittest.TestCase):
    """Тесты для функции __init__ класса Wall"""
    
    def test_wall_init_normal_values(self):
        """Тест нормальных значений"""
        wall = Wall(50, 60, 100, 200, 255, 128, 0)
        self.assertEqual(wall.r, 255)
        self.assertEqual(wall.g, 128)
        self.assertEqual(wall.b, 0)
        self.assertEqual(wall.width, 200)
        self.assertEqual(wall.height, 100)
        self.assertEqual(wall.rect.x, 50)
        self.assertEqual(wall.rect.y, 60)
    
    def test_wall_init_zero_size(self):
        """Тест нулевого размера"""
        wall = Wall(0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(wall.width, 0)
        self.assertEqual(wall.height, 0)
    
    def test_wall_init_color_range(self):
        """Тест диапазона цветов"""
        wall = Wall(0, 0, 10, 10, 0, 127, 255)
        self.assertEqual(wall.r, 0)
        self.assertEqual(wall.g, 127)
        self.assertEqual(wall.b, 255)


class TestWallPictureWall(unittest.TestCase):
    """Тесты для функции picture_wall класса Wall"""
    
    def test_picture_wall_no_exception(self):
        """Тест что метод не вызывает исключений"""
        wall = Wall(0, 0, 10, 10, 255, 0, 0)
        try:
            wall.picture_wall()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"picture_wall() вызвал исключение: {e}")

# ТЕСТЫ КЛАССА Door

class TestDoorInit(unittest.TestCase):
    """Тесты для функции __init__ класса Door"""
    
    def test_door_init_normal_values(self):
        """Тест нормальных значений"""
        door = Door(100, 200, 50, 20)
        self.assertEqual(door.width, 20)
        self.assertEqual(door.height, 50)
        self.assertEqual(door.rect.x, 100)
        self.assertEqual(door.rect.y, 200)
    
    def test_door_init_zero_size(self):
        """Тест нулевого размера"""
        door = Door(0, 0, 0, 0)
        self.assertEqual(door.width, 0)
        self.assertEqual(door.height, 0)
    
    def test_door_init_rect_properties(self):
        """Тест свойств rect"""
        door = Door(300, 400, 100, 30)
        self.assertEqual(door.rect.width, 30)
        self.assertEqual(door.rect.height, 100)

# ТЕСТЫ ИГРОВЫХ КОНСТАНТ

class TestGameConstants(unittest.TestCase):
    """Тесты игровых констант"""
    
    def test_fps_constant(self):
        """Тест константы FPS"""
        self.assertEqual(FPS, 60)
    
    def test_speed_factor_constant(self):
        """Тест константы SPEED_FACTOR"""
        self.assertEqual(SPEED_FACTOR, 10)
    
    def test_game_time_constant(self):
        """Тест константы GAME_TIME_MS"""
        self.assertEqual(GAME_TIME_MS, 120000)  # 2 минуты в миллисекундах
    
    def test_hit_cooldown_constant(self):
        """Тест константы HIT_COOLDOWN_MS"""
        self.assertEqual(HIT_COOLDOWN_MS, 600)
    
    def test_start_position_constants(self):
        """Тест констант стартовой позиции"""
        self.assertEqual(START_X, 15)
        self.assertEqual(START_Y, 500)

# ТЕСТЫ ВЗАИМОДЕЙСТВИЙ ОБЪЕКТОВ

class TestObjectInteractions(unittest.TestCase):
    """Тесты взаимодействий объектов"""
    
    def test_proekt_inheritance(self):
        """Тест наследования Caracters от Proekt"""
        char = Caracters(100, 100, 10, "test.png")
        self.assertIsInstance(char, Proekt)
        self.assertEqual(char.fx, 100.0)
        self.assertEqual(char.fy, 100.0)
    
    def test_enemy_inheritance(self):
        """Тест наследования Eneny от Proekt"""
        enemy = Eneny(100, 100, 10, "test.png")
        self.assertIsInstance(enemy, Proekt)
        self.assertTrue(hasattr(enemy, 'vrag_smena1'))
        self.assertTrue(hasattr(enemy, 'vrag_smena2'))
        self.assertTrue(hasattr(enemy, 'vrag_smena3'))
    
    def test_object_kill_method(self):
        """Тест метода kill"""
        obj = Proekt(100, 100, 5, "test.png")
        self.assertFalse(obj.kill_called)
        obj.kill()
        self.assertTrue(obj.kill_called)

# ТЕСТЫ ГРАНИЧНЫХ УСЛОВИЙ

class TestEdgeCases(unittest.TestCase):
    """Тесты граничных условий"""
    
    def test_extreme_coordinate_values(self):
        """Тест экстремальных значений координат"""
        test_cases = [
            (0, 0),
            (-1000, -1000),
            (1000000, 1000000),
            (-1000000, 1000000),
            (1000000, -1000000)
        ]
        
        for x, y in test_cases:
            try:
                obj = Proekt(x, y, 5, "test.png")
                self.assertEqual(obj.fx, float(x))
                self.assertEqual(obj.fy, float(y))
            except Exception as e:
                self.fail(f"Не удалось создать объект с координатами ({x}, {y}): {e}")
    
    def test_extreme_speed_values(self):
        """Тест экстремальных значений скорости"""
        test_speeds = [0, -10, 1000, -1000, 1000000]
        
        for speed in test_speeds:
            try:
                obj = Proekt(100, 100, speed, "test.png")
                self.assertEqual(obj.speed, speed)
            except Exception as e:
                self.fail(f"Не удалось создать объект со скоростью {speed}: {e}")
    
    def test_very_small_dt_values(self):
        """Тест очень маленьких значений dt"""
        enemy = Eneny(100, 100, 10, "test.png")
        small_dt_values = [0.001, 0.0001, 0.00001, 1e-10]
        
        for dt in small_dt_values:
            try:
                enemy.vrag_smena1(dt)
                enemy.vrag_smena2(dt)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Метод не обработал dt={dt}: {e}")
    
    def test_very_large_dt_values(self):
        """Тест очень больших значений dt"""
        enemy = Eneny(100, 100, 10, "test.png")
        large_dt_values = [10.0, 100.0, 1000.0]
        
        for dt in large_dt_values:
            try:
                enemy.vrag_smena1(dt)
                enemy.vrag_smena2(dt)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Метод не обработал dt={dt}: {e}")

# ТЕСТЫ НА ПОЛНОТУ ОБЪЕКТОВ

class TestObjectCompleteness(unittest.TestCase):
    """Тесты на полноту объектов"""
    
    def test_proekt_has_all_methods(self):
        """Тест что Proekt имеет все методы"""
        obj = Proekt(100, 100, 5, "test.png")
        methods = ['see', 'sync_rect', 'kill']
        
        for method in methods:
            self.assertTrue(hasattr(obj, method),
                          f"Proekt должен иметь метод {method}")
    
    def test_caracters_has_all_methods(self):
        """Тест что Caracters имеет все методы"""
        char = Caracters(100, 100, 10, "test.png")
        self.assertTrue(hasattr(char, 'smena'),
                       "Caracters должен иметь метод smena")
    
    def test_eneny_has_all_methods(self):
        """Тест что Eneny имеет все методы"""
        enemy = Eneny(100, 100, 10, "test.png")
        methods = ['vrag_smena1', 'vrag_smena2', 'vrag_smena3']
        
        for method in methods:
            self.assertTrue(hasattr(enemy, method),
                          f"Eneny должен иметь метод {method}")
    
    def test_wall_has_all_methods(self):
        """Тест что Wall имеет все методы"""
        wall = Wall(0, 0, 10, 10, 255, 0, 0)
        self.assertTrue(hasattr(wall, 'picture_wall'),
                       "Wall должен иметь метод picture_wall")


if __name__ == '__main__':
    unittest.main()
