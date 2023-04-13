import pygame
import random

pygame.init()

WIDTH, HEIGHT = 260, 550
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")


class Asset:
    """
    An enumeration of images used. This enumeration promotes better organization.
    """
    SUN = pygame.image.load('assets/sun.png').convert_alpha()
    MOON = pygame.image.load('assets/moon.png').convert_alpha()


class ThemedColour3:
    """
    The ThemedColour3 data type describes a colour using red, green, and blue components in the range of 0 to 255.
    Unlike a Colour3 data type, ThemedColour3 is used for themed colours.
    You don't have access to the red, green, and blue components, however the dark and light properties provide access
    to a tuple of these colours.
    """
    def __init__(self, dark_rgb, light_rgb):
        """
        Returns a ThemedColour3 with the given dark and light tints.
        The constructor takes as argument two tuples containing the red, green, and blue values in the range of 0 to 255.
        These two tuples correspond respectively to the dark then light tint.
        """
        self.dark = dark_rgb
        self.light = light_rgb

    def get(self, is_dark_theme):
        """
        Returns according to the boolean value passed in parameter a tuple in the format red, green, and blue.
        This tuple can be passed to pygame drawing functions when rendering.
        """
        if is_dark_theme:
            return self.dark

        return self.light


class Colour:
    """
    An enumeration of the colours used. This enumeration promotes better organization.
    """
    BLACK = ThemedColour3((24, 24, 27), (234, 234, 236))
    WHITE = ThemedColour3((234, 234, 236), (24, 24, 27))
    BLUE = ThemedColour3((88, 101, 242), (88, 101, 242))
    GREEN = ThemedColour3((87, 242, 135), (87, 242, 135))
    YELLOW = ThemedColour3((254, 231, 92), (254, 231, 92))
    ORANGE = ThemedColour3((255, 150, 79), (255, 150, 79))
    RED = ThemedColour3((237, 66, 69), (237, 66, 69))
    PINK = ThemedColour3((235, 69, 158), (235, 69, 158))

    # This value can be removed from the enumeration in favor of a global variable or at the beginning of the file,
    # however it allows a certain rigor in the access to colour information
    IS_DARK_THEME = True
    IS_EPILEPTIC_MODE = False


class Button:
    """
    The main element of the game interface, this class represents a button and greatly facilitates the management of
    these.
    It allows you to display and manage almost the entire game.
    """
    def __init__(self, position, colour=Colour.BLACK, border=Colour.WHITE, image=None):
        """
        Returns a Button with the given properties.
        """
        self.px, self.py = position
        self.sx, self.sy = (30, 30)

        self.rect = pygame.Rect((self.px, self.py), (self.sx, self.sy))

        self.set_image(image)
        self.set_fill_colour(colour)
        self.set_border_colour(border)

    def set_fill_colour(self, colour):
        """
        Sets the background colour of a button.
        The use of this function is optional, it is possible to directly define the property despite a less readable
        code.
        """
        self.colour = colour

    def set_border_colour(self, colour):
        """
        Sets the border colour of a button.
        The use of this function is optional, it is possible to directly define the property despite a less readable
        code.
        """
        self.border_colour = colour

    def set_image(self, image):
        """
        Sets the image of a button.
        If no image is specified, simply delete the previous one.
        """
        if image is None:
            self.image = None
            return

        px = self.px + self.sx / 2
        py = self.py + self.sy / 2

        self.image = image
        self.img_rect = image.get_rect(center=(px, py))

    def collidepoint(self, position):
        """
        Syntax-saving shortcut function.
        """
        return self.rect.collidepoint(position)

    def render(self):
        """
        Manage button rendering.
        """
        pygame.draw.rect(window, self.border_colour.get(Colour.IS_DARK_THEME), (self.px, self.py, self.sx, self.sy), 1)
        pygame.draw.rect(window, self.colour.get(Colour.IS_DARK_THEME), (self.px + 3, self.py + 3, self.sx - 6, self.sx - 6))

        # Skips image rendering if none has been specified.
        if self.image is not None:
            window.blit(self.image, self.img_rect)


class Mastermind:
    """
    Entry point of the game, it allows management of logic, rendering and data storage of the game.
    """
    def __init__(self):
        """
        Initiate the default singleton properties then start the main loop.
        """
        self.theme_button = Button((WIDTH - 40, 510), image=Asset.SUN)
        self.easter_click = 0

        # Select the default colour, the colour black corresponds to the default colour of the game board. Thus it
        # corresponds to selecting no colour.
        # The colour is defined here and not in the restart method so that the colour of the previous game is kept
        # during a new game.
        self.selected_colour = Colour.BLACK

        self.restart()
        self.start_tick()

    def start_tick(self):
        """
        Function that initializes the game loop.
        """
        self.running = True

        while self.running:
            self.tick()

        pygame.quit()

    def tick(self):
        """
        Main function of the game, it is called at each iteration and calls the various parts of the project, rendering,
        management of keys, management of endgames, ...
        """
        self.process_events()

        # Verification of defeat must be done separately from victory in order to avoid an error if we fail to crack the
        # code
        if self.current_turn >= 12:
            self.gameover = True

        # Execute line check logic when condition is met
        if not self.gameover and self.is_line_complete():
            good, bad = self.verify()
            self.hints[self.current_turn] = (good, bad)

            if good == 4:
                self.gameover = True

            self.current_turn += 1

        window.fill(Colour.BLACK.get(Colour.IS_DARK_THEME))
        if Colour.IS_EPILEPTIC_MODE:
            window.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        self.render()

        pygame.display.flip()

    def render(self):
        """
        Function managing graphic rendering, any rendering performed must be initiated in this function.
        """
        for line in self.grid:
            for button in line:
                button.render()

        for button in self.toolbar:
            button.render()

        self.render_hints()
        self.render_secret_code()

        self.theme_button.render()

    def render_secret_code(self):
        """
        Secret code specific rendering function.
        """
        y_pos = 510

        for x in range(4):
            x_pos = 10 + 40 * x

            pygame.draw.rect(window, Colour.WHITE.get(Colour.IS_DARK_THEME), (x_pos, y_pos, 30, 30), 1)

            if self.gameover:
                pygame.draw.rect(window, self.code[x].get(Colour.IS_DARK_THEME), (x_pos + 3, y_pos + 3, 24, 24))

    def render_hints(self):
        """
        Hints specific rendering function.
        """
        x_pos = 170
        for y, hint in enumerate(self.hints):
            good, bad = hint

            y_pos = 10 + 40 * y

            # Draw borders
            pygame.draw.rect(window, Colour.WHITE.get(Colour.IS_DARK_THEME), (x_pos, y_pos, 12, 12), 1)
            pygame.draw.rect(window, Colour.WHITE.get(Colour.IS_DARK_THEME), (x_pos + 18, y_pos, 12, 12), 1)
            pygame.draw.rect(window, Colour.WHITE.get(Colour.IS_DARK_THEME), (x_pos, y_pos + 18, 12, 12), 1)
            pygame.draw.rect(window, Colour.WHITE.get(Colour.IS_DARK_THEME), (x_pos + 18, y_pos + 18, 12, 12), 1)

            # Generates a list of colours to draw.
            colours_to_draw = []
            colours_to_draw.extend([Colour.WHITE] * good)
            colours_to_draw.extend([Colour.RED] * bad)
            colours_to_draw.extend([Colour.BLACK] * (4 - len(colours_to_draw)))

            # Draw backgrounds
            pygame.draw.rect(window, colours_to_draw.pop(0).get(Colour.IS_DARK_THEME), (x_pos + 2, y_pos + 2, 8, 8))
            pygame.draw.rect(window, colours_to_draw.pop(0).get(Colour.IS_DARK_THEME), (x_pos + 20, y_pos + 2, 8, 8))
            pygame.draw.rect(window, colours_to_draw.pop(0).get(Colour.IS_DARK_THEME), (x_pos + 2, y_pos + 20, 8, 8))
            pygame.draw.rect(window, colours_to_draw.pop(0).get(Colour.IS_DARK_THEME), (x_pos + 20, y_pos + 20, 8, 8))

    def process_events(self):
        """
        Process pygame related events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()

    def handle_click(self, event):
        """
        Specifically handle the event of a mouse click.
        The pygame event must be provided to the function in order to access information about it.
        """
        position = event.pos

        if self.theme_button.collidepoint(position):
            Colour.IS_DARK_THEME = not Colour.IS_DARK_THEME
            self.theme_button.set_image(Asset.SUN if Colour.IS_DARK_THEME else Asset.MOON)

            self.easter_click += 1
            if self.easter_click >= 10:
                Colour.IS_EPILEPTIC_MODE = True
            return

        # If another click occurs not on the button, the easter egg is canceled
        self.easter_click = 0

        # The buttons located after this condition are useful only when a game is in progress.
        if self.gameover:
            return

        for button in self.toolbar:
            if button.collidepoint(position):
                self.selected_colour = button.colour
                return

        line = self.grid[self.current_turn]
        for button in line:
            if button.collidepoint(position):
                button.set_fill_colour(self.selected_colour)
                return

    def verify(self):
        """
        Verifies the current line and returns these statistics.
        """
        secret_code = self.code.copy()
        code = [button.colour for button in self.grid[self.current_turn]]
        good, bad = 0, 0

        for index, colour in enumerate(code):
            if secret_code[index] == colour:
                good += 1
                code[index] = 0
                secret_code[index] = None

        for index, colour in enumerate(code):
            if colour in secret_code:
                bad += 1
                secret_code[secret_code.index(colour)] = None

        return good, bad

    def is_line_complete(self):
        """
        Returns a value corresponding to the status of the current line, whether it is completed or not.
        """
        completed = True

        line = self.grid[self.current_turn]
        for button in line:
            if button.colour == Colour.BLACK:
                completed = False

        return completed

    def restart(self):
        """
        Resets the variables specific to each game.
        """
        colours = [Colour.BLUE, Colour.GREEN, Colour.YELLOW, Colour.ORANGE, Colour.RED, Colour.PINK]

        self.code = [random.choice(colours) for _ in range(4)]
        self.current_turn = 0

        self.hints = [(0, 0) for _ in range(12)]
        self.gameover = False

        self.grid = []
        self.toolbar = []

        # Initialize game board buttons
        for y in range(12):
            y_pos = 10 + 40 * y
            line = []
            for x in range(4):
                x_pos = 10 + 40 * x
                button = Button((x_pos, y_pos))
                line.append(button)
            self.grid.append(line)

        # Initialize toolbar buttons
        x_pos = WIDTH - 40
        margin = (HEIGHT - 230 - 60) / 2
        for y in range(6):
            y_pos = margin + 40 * y
            button = Button((x_pos, y_pos), colours[y])
            self.toolbar.append(button)


if __name__ == "__main__":
    mastermind = Mastermind()