import numpy as np
import pygame
import random
import math

class TextureGenerator:
    @staticmethod
    def create_texture(base_color, style="default", size=(64, 64)):
        # Style-specific noise ranges
        style_ranges = {
            'default':        (-20, 20),
            'smooth_stone':   (-10, 10),
            'rough_stone':    (-25, 25),
            'white_stone':    (-8, 8),
            'dark_red':       (-15, 15),
            'lava_stone':     (-15, 15),
        }
        low, high = style_ranges.get(style, style_ranges['default'])
        w, h = size

        # Generate base noise
        noise = np.random.randint(low, high + 1, size=(h, w), dtype=np.int16)
        r, g, b = base_color

        # Apply style-specific masks
        if style == 'dark_red':
            dark_mask = np.random.random((h, w)) < 0.01
            noise[dark_mask] -= 20
        elif style == 'lava_stone':
            glow_mask = np.random.random((h, w)) < 0.06
            # Lava glow effect: boost red channel, dim green/blue
            glow = np.zeros((h, w, 3), dtype=np.int16)
            glow[..., 0] = np.random.randint(30, 61, size=(h, w))
            glow[..., 1] = -10
            glow[..., 2] = -15

        # Create color channels
        chan_r = np.clip(r + noise, 0, 255).astype(np.uint8)
        chan_g = np.clip(g + noise, 0, 255).astype(np.uint8)
        chan_b = np.clip(b + noise, 0, 255).astype(np.uint8)

        arr = np.dstack([chan_r, chan_g, chan_b])

        # Apply lava glow after stacking
        if style == 'lava_stone':
            arr = arr.astype(np.int16)
            arr += glow
            arr = np.clip(arr, 0, 255).astype(np.uint8)

        # Build surface
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.surfarray.blit_array(surface, arr.transpose((1, 0, 2)))
        return surface

    @staticmethod
    def create_wood_texture(size=(64, 64), base_color=(160, 82, 45)):

        w, h = size
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        xv, yv = np.meshgrid(x, y)

        # Very soft variation across surface
        gradient = (
            10 * (np.sin(2 * np.pi * xv * np.random.uniform(0.5, 1.0)) +
                np.sin(2 * np.pi * yv * np.random.uniform(0.5, 1.0)))
        )

        # Subtle random noise to prevent flatness
        noise = (np.random.rand(h, w) - 0.5) * 5
        pattern = gradient + noise

        # Build color array
        r, g, b = base_color
        arr = np.dstack([
            np.clip(r + pattern, 0, 255),
            np.clip(g + pattern, 0, 255),
            np.clip(b + pattern, 0, 255)
        ]).astype(np.uint8)

        # Create the surface
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.surfarray.blit_array(surface, arr.transpose((1, 0, 2)))
        return surface

    @staticmethod
    def create_ice_texture(size=(64, 64), base_color=(220, 235, 245)):
        w, h = size
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        xv, yv = np.meshgrid(x, y)

        # Very soft gradient noise
        gradient = (
            10 * (np.sin(2 * np.pi * xv * np.random.uniform(1, 2)) +
                np.sin(2 * np.pi * yv * np.random.uniform(1, 2)))
        )

        # Add some subtle perlin-like noise
        noise = (np.random.rand(h, w) - 0.5) * 5
        pattern = gradient + noise

        # Optional gentle sparkles
        sparkle_mask = np.random.random((h, w)) < 0.01
        sparkle_intensity = np.random.uniform(20, 40, (h, w))
        pattern += sparkle_mask * sparkle_intensity

        # Build RGB array
        r, g, b = base_color
        arr = np.dstack([
            np.clip(r + pattern, 0, 255),
            np.clip(g + pattern, 0, 255),
            np.clip(b + pattern, 0, 255)
        ]).astype(np.uint8)

        # Create the surface
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.surfarray.blit_array(surface, arr.transpose((1, 0, 2)))
        return surface

    @staticmethod
    def create_stone_texture(size=(64, 64), base_color=(130, 130, 130)):
        """
        Create a smooth stone-like texture with soft color gradients.

        Args:
            size (tuple[int, int]): Width and height.
            base_color (tuple[int, int, int]): RGB stone color.
        Returns:
            pygame.Surface
        """
        w, h = size
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        xv, yv = np.meshgrid(x, y)

        # Very gentle gradient waves
        gradient = (
            8 * (np.sin(2 * np.pi * xv * np.random.uniform(0.5, 1.0)) +
                np.sin(2 * np.pi * yv * np.random.uniform(0.5, 1.0)))
        )

        # Very light noise
        noise = (np.random.rand(h, w) - 0.5) * 4
        pattern = gradient + noise

        # Build the RGB array
        r, g, b = base_color
        arr = np.dstack([
            np.clip(r + pattern, 0, 255),
            np.clip(g + pattern, 0, 255),
            np.clip(b + pattern, 0, 255)
        ]).astype(np.uint8)

        # Create the surface
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.surfarray.blit_array(surface, arr.transpose((1, 0, 2)))
        return surface
    @staticmethod
    def create_crack_texture(intensity, size=(64, 64)):
        w, h = size
        surface = pygame.Surface((w, h), pygame.SRCALPHA)

        # Make number of cracks grow non-linearly (exponentially)
        num_main_cracks = int((intensity ** 2) * 40)  # square the intensity

        for _ in range(num_main_cracks):
            start = (random.randint(0, w-1), random.randint(0, h-1))
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(20, 40)

            points = [start]
            current_pos = start
            current_angle = angle

            for _ in range(length):
                current_angle += random.uniform(-0.15, 0.15)
                new_x = int(current_pos[0] + math.cos(current_angle) * 2)
                new_y = int(current_pos[1] + math.sin(current_angle) * 2)

                if 0 <= new_x < w and 0 <= new_y < h:
                    current_pos = (new_x, new_y)
                    points.append(current_pos)

                    if random.random() < 0.02:
                        branch_angle = current_angle + random.choice([-math.pi/4, math.pi/4])
                        branch_length = random.randint(5, 15)
                        branch_points = [current_pos]
                        branch_pos = current_pos
                        branch_dir = branch_angle
                        for _ in range(branch_length):
                            branch_dir += random.uniform(-0.2, 0.2)
                            bx = int(branch_pos[0] + math.cos(branch_dir) * 2)
                            by = int(branch_pos[1] + math.sin(branch_dir) * 2)
                            if 0 <= bx < w and 0 <= by < h:
                                branch_pos = (bx, by)
                                branch_points.append(branch_pos)
                            else:
                                break
                        if len(branch_points) > 1:
                            pygame.draw.aalines(surface, (0, 0, 0, 150), False, branch_points)

            if len(points) > 1:
                pygame.draw.aalines(surface, (0, 0, 0, 180), False, points)

        return surface
            
    def upgrade_crack_texture(surface, old_intensity, new_intensity, size=(64, 64)):
        w, h = size

        # Calculate how many more cracks we need based on the difference
        additional_intensity = new_intensity ** 2 - old_intensity ** 2
        additional_cracks = int(additional_intensity * 40)

        for _ in range(additional_cracks):
            start = (random.randint(0, w-1), random.randint(0, h-1))
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(20, 40)

            points = [start]
            current_pos = start
            current_angle = angle

            for _ in range(length):
                current_angle += random.uniform(-0.15, 0.15)
                new_x = int(current_pos[0] + math.cos(current_angle) * 2)
                new_y = int(current_pos[1] + math.sin(current_angle) * 2)

                if 0 <= new_x < w and 0 <= new_y < h:
                    current_pos = (new_x, new_y)
                    points.append(current_pos)

                    if random.random() < 0.02:
                        branch_angle = current_angle + random.choice([-math.pi/4, math.pi/4])
                        branch_length = random.randint(5, 15)
                        branch_points = [current_pos]
                        branch_pos = current_pos
                        branch_dir = branch_angle
                        for _ in range(branch_length):
                            branch_dir += random.uniform(-0.2, 0.2)
                            bx = int(branch_pos[0] + math.cos(branch_dir) * 2)
                            by = int(branch_pos[1] + math.sin(branch_dir) * 2)
                            if 0 <= bx < w and 0 <= by < h:
                                branch_pos = (bx, by)
                                branch_points.append(branch_pos)
                            else:
                                break
                        if len(branch_points) > 1:
                            pygame.draw.aalines(surface, (0, 0, 0, 150), False, branch_points)

            if len(points) > 1:
                pygame.draw.aalines(surface, (0, 0, 0, 180), False, points)

        return surface
