import pygame
import sys
import random


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "serie_05_exercice_01" # Titre de la fenêtre du jeu
# Définir le demi-décalage et l'épaisseur des bords de la fenêtre de jeu
WINDOW_BORDER_LINE_OFFSET = 10
# Liste des bords où le rebond est possible
WINDOW_BORDERS_NAME: list[str] = ["left", "right"]
# Couleur des bords
WINDOW_BORDERS_COLOR: dict[str, str] = {"left" : "red", "right" : "blue", "top" : "yellow", "bottom" : "grey"}
FPS: int = 24 # Frame Per Second = taux de rafraîchissement de l'affichage par seconde


# Définir la classe des acteurs
class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2

    '''
    Série 05 Exercice 1
        a) Pour quelle raison l’attribut `_size` a-t-il disparu de la classe `Actor` et où est-il allé ?
    
        # RÉPONSE #
        L'attribut _size a disparu, car
        …
        et il est allé
        …
    '''
    
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        self._position = position
        self._speed = speed

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    def _move(self) -> None:
        self._position += self._speed

    def update(self) -> None:
        self._move()


class Spaceship(Actor):
    __size: pygame.Vector2

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__size = size

    @property
    def size(self) -> pygame.Vector2:
        return self.__size


class Asteroid(Actor):
    __diameter: int

    def __init__(self, position: pygame.Vector2, diameter: int, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__diameter = diameter

    @property
    def diameter(self) -> int:
        return self.__diameter

    @property
    def radius(self) -> int:
        return self.__diameter // 2


# Définir la classe des sprites des acteurs
# class ActorPseudoSprite():
class ActorSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface # Image de l'acteur
    _rect: pygame.Rect     # Rectangle de déplacement de l'image

    # Python autorise des paramètres dont le nombre varie
    # entre 0 et une valeur arbitraire, dans ce cas, ils sont
    # précédés d'une étoile (*args est souvent utilisé)

    # Un pygame.sprite.Sprite peut appartenir à aucun, un ou
    # plusieurs pygame.sprite.Group
    def __init__(self, actor: Actor, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self._actor = actor
        self._color = color
        self._init_image()
        self._init_rect()

    # Getter nécessaire pour la classe Game
    @property
    def actor(self) -> Actor:
        return self._actor

    @property
    def color(self) -> pygame.Color:
        return self._color

    @color.setter
    def color(self, color: pygame.Color) -> None:
        self._color = color

    # Getter nécessaire pour la classe pygame.sprite.Group
    @property
    def image(self) -> pygame.Surface:
        return self._image

    # Getter nécessaire pour gérer les collisions
    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    '''
    Série 05 Exercice 1
        b) Quel est l’objectif de déclarer trois méthodes qui retournent une erreur dans la classe `ActorSprite` ?
        
        # RÉPONSE #
        Les trois prochaines méthodes sont là, car
        …
    '''

    # Définir l'image affichée pour l'acteur
    def _init_image(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter _init_image()")

    def paint_image(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter paint_image()")

    # La méthode update() est utilisée par pygame.Sprite.Group
    def update(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter update()")

    # Définir le rectangle qui recevra l'image de l'acteur
    '''
    Série 05 Exercice 1
        c) En revanche, pour quelle raison la méthode `_init_rect()` peut-elle rester dans la classe `ActorSprite` ?    
        
        # RÉPONSE #
        Cette méthode peut rester telle quelle dans la classe mère, car
        …
    '''
    def _init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self._rect = self._image.get_rect()
        # Le placer à l'endroit de l'acteur
        self._rect.update(self._actor.position, self._rect.size)


class SpaceshipSprite(ActorSprite):
    _actor: Spaceship

    '''
    Série 05 Exercice 1
        d) Les sous-classes SpaceshipSprite et AsteroidSprite redéclare l’attribut _actor en modifiant son type.
           Mettez cette redéclaration en commentaire (ajouter un # devant _actor) pour la sous-classe`SpaceshipSprite`.
           Observez ce qui se passe dans les différentes méthodes de cette sous-classe.
           En principe, votre IDE (VS Code) devrait vous indiquer qu’il détecte un problème au niveau de `self._actor.size`, pourquoi ?    
        
        # RÉPONSE #
        Il y a un problème, car `self._actor.size` 
        …

        e) Décommentez cette redéclaration (enlever le # devant _actor) dans la sous-classe `SpaceshipSprite`.
    '''

    '''
    Série 05 Exercice 1
        f) Supposez que vous souhaitiez imposer la couleur magenta à la sous-classe SpaceshipSprite
           en conservant uniquement le paramètre spaceship: Spaceship dans le constructeur.
           Effectuez le minimum de modifications dans le code pour que cela fonctionne.
           Nommez éventuellement les modifications auxquelles vous n’aviez pas initialement pensé.
           
        # RÉPONSES #
        * CODE COMMENTÉ *
        Il faut faire attention à
        …
    '''
    def __init__(self, spaceship: Spaceship, color: pygame.Color) -> None:
        super().__init__(spaceship, color)

    def _init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self._image = pygame.Surface(self._actor.size)
        self.paint_image()

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, self._actor.size)

    # Dessin de la représentation du spaceship
    def paint_image(self) -> None:
        # Dessiner sur l'image une ellipse de la couleur choisie à la création de l'image
        pygame.draw.ellipse(self._image, self._color, ((0, 0), self._actor.size))


class AsteroidSprite(ActorSprite):
    _actor: Asteroid

    def __init__(self, asteroid: Asteroid, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(asteroid, color, *groups)

    def _init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self._image = pygame.Surface((self._actor.diameter, self._actor.diameter))
        # Dessiner la représentation de l'acteur
        self.paint_image()

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, (self._actor.diameter, self._actor.diameter))

    # Dessin de la représentation des astéroïdes
    def paint_image(self) -> None:
        # Dessiner sur l'image un cercle de la couleur choisie à la création de l'image
        pygame.draw.circle(self._image, self._color, (self._actor.radius, self._actor.radius), self._actor.radius, width = 1)


class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __frame_counter: int
    __spaceship_sprite: pygame.sprite.GroupSingle
    __asteroids_sprites: pygame.sprite.Group
    __borders_collision_sprites: pygame.sprite.Group

    '''
        Série 05 Exercice 1
            g) Quelle pourrait être l’utilité de l’attribut `__frame_counter` dans la classe `Game` ?
            
            # RÉPONSES #
            `__frame_counter` va permettre de
            …
    '''

    '''
        Série 05 Exercice 1
            h) Améliorez les commentaires de la classe `Game` pour que vous soyez en mesure de la comprendre.
            
            # RÉPONSES #
            * CODE COMMENTÉ *
    '''

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()
        self.__init_actors()
     
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    # Initialiser les acteurs et leurs sprites
    def __init_spaceship(self) -> None:
        spaceship = Spaceship(
                       pygame.Vector2(180 - 60 / 2, 360 - 45),
                       pygame.Vector2(60, 45),
                       pygame.Vector2(-5, 0)
                     )
        spaceship_sprite = SpaceshipSprite(spaceship, pygame.Color(pygame.color.THECOLORS["magenta"]))
        self.__spaceship_sprite = pygame.sprite.GroupSingle(spaceship_sprite)
        self.__borders_collision_sprites.add(self.__spaceship_sprite)

    def __init_asteroids(self) -> None:
        self.__asteroids_sprites = pygame.sprite.Group()
        for i in range(16):
            radius = random.randint(1, 3)
            asteroid = Asteroid(
                pygame.Vector2(10 + 25 * i + radius, radius),
                10 * radius,
                pygame.Vector2(random.randint(-2, 2), random.randint(1, 2))
            )
            AsteroidSprite(asteroid, pygame.Color(pygame.color.THECOLORS["cyan"]), self.__asteroids_sprites, self.__borders_collision_sprites)

    def __init_actors(self) -> None:
        self.__borders_collision_sprites = pygame.sprite.Group()
        self.__init_spaceship()
        self.__init_asteroids()

    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            # Terminer le processus Python
            sys.exit()

    # Créer les lignes des bords de l'écran
    def __draw_screen_borders(self) -> None:
        # Initialiser le dictionnaire des lignes des bords
        self.__screen_borders_lines = {}
        # Récupérer le rectangle de l'écran
        screen_rect = self.__screen.get_rect()
        # Définir les caractéristiques des bords
        screen_borders = {
                          "left":   {"offset": pygame.Vector2(+1, 0), "start": screen_rect.topleft,    "end": screen_rect.bottomleft},
                          "right":  {"offset": pygame.Vector2(-1, 0), "start": screen_rect.topright,   "end": screen_rect.bottomright},
                          "top":    {"offset": pygame.Vector2(0, +1), "start": screen_rect.topleft,    "end": screen_rect.topright },
                          "bottom": {"offset": pygame.Vector2(0, -1), "start": screen_rect.bottomleft, "end": screen_rect.bottomright}
        }
        # Boucle de création des bords
        for border_name in WINDOW_BORDERS_NAME:
            # Calcul du décalage intérieur
            offset = WINDOW_BORDER_LINE_OFFSET * screen_borders[border_name]["offset"] // 2
            # Dessin de la ligne concerné avec ajour direct dans le dictionnaire des bords
            border_line = pygame.draw.line(
                self.__screen,
                pygame.color.THECOLORS[WINDOW_BORDERS_COLOR[border_name]],
                pygame.Vector2(screen_borders[border_name]["start"]) + offset,
                pygame.Vector2(screen_borders[border_name]["end"]) + offset,
                width = WINDOW_BORDER_LINE_OFFSET
            )
            self.__screen_borders_lines[border_name] = border_line

    # Détecter la collision avec la bordure droite
    # en utilisant la détection de collision entre rectangles
    def __handle_borders_collisions(self) -> None:
        for actor_sprite in self.__borders_collision_sprites:
            for screen_border_name, screen_border_line in self.__screen_borders_lines.items():
                if actor_sprite.rect.colliderect(screen_border_line):
                    if screen_border_name == "left" and actor_sprite.actor.speed.x < 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "right" and actor_sprite.actor.speed.x > 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "top" and actor_sprite.actor.speed.y < 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y
                    if screen_border_name == "bottom" and actor_sprite.actor.speed.y > 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y

    # Détecter les collisions entre le spaceship et les asteroids
    def __handle_spaceship_collisions_with_asteroids(self):
        hinted_asteroids_sprites = pygame.sprite.groupcollide(self.__asteroids_sprites, self.__spaceship_sprite, False, False)
        for hinted_asteroid_sprite in hinted_asteroids_sprites:
            hinted_asteroid_sprite.color = pygame.color.THECOLORS["yellow"]
            hinted_asteroid_sprite.paint_image()

    def __handle_collisions(self):
        self.__handle_borders_collisions()
        self.__handle_spaceship_collisions_with_asteroids()

    # Mettre à jour les sprites des acteurs
    def __update_actors(self) -> None:
        self.__spaceship_sprite.update()
        self.__asteroids_sprites.update()

    # Dessiner les sprites des acteurs
    def __draw_actors(self) -> None:
        self.__spaceship_sprite.draw(self.__screen)
        self.__asteroids_sprites.draw(self.__screen)

    def run(self) -> None:
        self.__is_running = True
        self.__frame_counter = 0
        while self.__is_running:
            # Maintenir le taux de rafraîchissement
            self.__clock.tick_busy_loop(FPS)
            self.__frame_counter += 1
            for event in pygame.event.get():
                self.__handle_events(event)
            # Remplir le fonds de l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])
            # Dessiner les bords
            self.__draw_screen_borders()
            # Gérer les collisions
            self.__handle_collisions()
            # Mettre à jour les acteurs
            self.__update_actors()
            # Dessiner les acteurs
            self.__draw_actors()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()


# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
