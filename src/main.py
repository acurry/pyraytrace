import numpy as np
import matplotlib.pyplot as plt

from scene import Scene, Shape

OUTPUT_DIR = './output'

def normalize(vector: np.ndarray):
    return vector / np.linalg.norm(vector)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center)**2 - radius**2
    delta = b**2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def nearest_intersected_object(shapes: list[Shape], ray_origin, ray_direction):
    distances = [
        sphere_intersect(obj.center, obj.radius, ray_origin,
                         ray_direction) for obj in shapes
    ]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = shapes[index]
    return nearest_object, min_distance


def main():
    SCENE = Scene.init_from_file("./src/scene_sample1.yaml")

    camera = np.array(SCENE.camera)

    image = np.zeros((SCENE.height, SCENE.width, 3))
    for i, y in enumerate(np.linspace(SCENE.screen['top'], SCENE.screen['bottom'], SCENE.height)):
        for j, x in enumerate(np.linspace(SCENE.screen['left'], SCENE.screen['right'], SCENE.width)):
            # screen is on origin
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)

            color = np.zeros((3))
            reflection = 1

            for k in range(SCENE.max_depth):
                # check for intersections
                nearest_object, min_distance = nearest_intersected_object(
                    SCENE.shapes, origin, direction)
                if nearest_object is None:
                    break

                intersection = origin + min_distance * direction
                normal_to_surface = normalize(intersection -
                                              nearest_object.center)
                shifted_point = intersection + 1e-5 * normal_to_surface
                intersection_to_light = normalize(SCENE.light.position -
                                                  shifted_point)

                _, min_distance = nearest_intersected_object(
                    SCENE.shapes, shifted_point, intersection_to_light)
                intersection_to_light_distance = np.linalg.norm(
                    SCENE.light.position - intersection)
                is_shadowed = min_distance < intersection_to_light_distance

                if is_shadowed:
                    break

                illumination = np.zeros((3))

                # ambiant
                illumination += nearest_object.ambient * SCENE.light.ambient

                # diffuse
                illumination += nearest_object.diffuse * SCENE.light.diffuse * np.dot(
                        intersection_to_light, normal_to_surface)

                # specular
                intersection_to_camera = normalize(camera - intersection)
                H = normalize(intersection_to_light + intersection_to_camera)
                illumination += nearest_object.specular * SCENE.light.specular * np.dot(normal_to_surface, H)**(float(nearest_object.shininess) / 4.0)

                # reflection
                color += reflection * illumination
                reflection *= nearest_object.reflection

                origin = shifted_point
                direction = reflected(direction, normal_to_surface)

            image[i, j] = np.clip(color, 0, 1)

    filename = f"{SCENE.width}x{SCENE.height}_depth_{SCENE.max_depth}_shapes_{len(SCENE.shapes)}.png"
    plt.imsave(f'{OUTPUT_DIR}/{filename}', image)


if __name__ == "__main__":
    main()
