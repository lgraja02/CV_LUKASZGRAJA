#include <SDL.h>
#include <stdio.h>
#include <stdbool.h>
#include <SDL_ttf.h>
#include <time.h>
#include <string.h>
#include <SDL_mixer.h>

#define WINDOW_WIDTH 1100
#define WINDOW_HEIGHT 588
#define FONT_SIZE 100

SDL_Surface* loadSurface(const char* path);
void renderButton(SDL_Surface* buttonSurface, SDL_Surface* surface, int x, int y, int width, int height);
void renderText(SDL_Surface* surface, const char* text, int x, int y, TTF_Font* font, SDL_Color color);

int main(int argc, char* args[]) {
    //sprawdzanie czy dziala biblioteka SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }
    //tworzenie okna
    SDL_Window* window = SDL_CreateWindow("wisielec", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    //tworzenie powierzchni okna
    SDL_Surface* surface = SDL_GetWindowSurface(window);
    if (!surface) {
        printf("Surface could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    //ladowanie tla okna
    SDL_Surface* backgroundSurface = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Background.bmp");
    if (!backgroundSurface) {
        printf("Failed to load background image! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Inicjalizacja SDL_mixer
    if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048) < 0) {
        printf("SDL_mixer could not initialize! SDL_mixer Error: %s\n", Mix_GetError());
        return 5;
    }

    // Wczytanie pliku muzycznego
    Mix_Music* backgroundMusic = Mix_LoadMUS("tekstury/Background_Music.mp3");
    if (!backgroundMusic) {
        printf("Failed to load background music! SDL_mixer Error: %s\n", Mix_GetError());
        return 4;
    }


    // Wczytanie obrazu wisielca
    SDL_Surface* wisielec0 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec0.bmp");
    SDL_Surface* wisielec1 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec1.bmp");
    SDL_Surface* wisielec2 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec2.bmp");
    SDL_Surface* wisielec3 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec3.bmp");
    SDL_Surface* wisielec4 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec4.bmp");
    SDL_Surface* wisielec5 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec6.bmp");
    SDL_Surface* wisielec6 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec8.bmp");
    SDL_Surface* wisielec7 = SDL_LoadBMP("tekstury/Wisielec_Obrazy/Wisielec10.bmp");
    if (!wisielec0 && !wisielec1 && !wisielec2 && !wisielec3 && !wisielec4 && !wisielec5 && !wisielec6 && !wisielec7) {
        printf("Failed to load image! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Ustawienie położenia obrazu 
    SDL_Rect imageRect;
    imageRect.x = 690;  // Współrzędna x, gdzie obrazek ma być renderowany
    imageRect.y = 20;   // Współrzędna y, gdzie obrazek ma być renderowany


//    imageRect.x = 950;  // Współrzędna x, gdzie obrazek ma być renderowany
//    imageRect.y = 120;   // Współrzędna y, gdzie obrazek ma być renderowany


    Mix_PlayMusic(backgroundMusic, -1);

    //kopiowanie zawartosci powierzchni 1- zrodlo kopiowania 2/4-NULL cala powierzchnia ma byc kopiowana 3-surface docelowa powierzchnia na ktorej ma byc wyrenderowane
    SDL_BlitSurface(backgroundSurface, NULL, surface, NULL);

    //ladowanie przyciskow
    SDL_Surface* playButtonSurface = loadSurface("tekstury/Buttons/Play_Button.bmp");
    SDL_Surface* exitButtonSurface = loadSurface("tekstury/Buttons/Exit.bmp");
    SDL_Surface* muteButtonSurface = loadSurface("tekstury/Buttons/Mute_Button.bmp");
    //generowanie przyciskow na ekranie (x,y,width,height)
//    renderButton(playButtonSurface, surface, 470, 400, 234, 84);
//    renderButton(exitButtonSurface, surface, 740, 400, 234, 84);
//    renderButton(muteButtonSurface, surface, 0, 0, 70, 70);

    SDL_UpdateWindowSurface(window);
    //inicjalizacja biblioteki SDL2_TTF
    TTF_Init();
    //zaladowanie fontow
    TTF_Font* font = TTF_OpenFont("Creepster-Regular.ttf", FONT_SIZE);
    if (!font) {
        printf("Failed to load font! SDL_Error: %s\n", TTF_GetError());
        return 1;
    }



    bool quit = false;
    bool playClicked = false, isGuessed = false, isWypisane = false, czyWygrales = false, czyPrzegrales = false, musicplay = true;
    char inputText[100] = ""; // Przechowuje wprowadzony tekst
    char AktualnyTekst[100]="";

    //10 IS MAX  WORD LENGHT!!!!!!!!!!!!!!!!!!!
    char words[100][100] = {"finger", "finish", "fire", "firm", "first", "fish", "five", "floor", "flyhigh", "him", "himself", "his", "history", "hit", "hold", "home", "hope", "hospital", "hot", "hotel", "hour", "language", "large", "last", "late", "later", "laugh", "law", "lawyer", "lay", "lead", "leader", "main", "maintain", "major", "majority", "make", "man", "manage", "management", "manager", "many", "market", "marriage", "material", "matter", "may", "off", "offer", "office", "officer", "official", "often", "oh", "oil", "ok", "old", "on", "once", "one", "private", "probably", "problem", "process", "produce", "product", "production", "professional", "professor", "program", "project", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report", "since", "sing", "single", "sister", "sit", "site", "situation", "six", "size", "skill", "skin", "small", "smile", "strong", "structure", "student", "study", "stuff", "style", "subject", "success", "successful", "such", "suddenly", "suffer", "suggest", "summer", "write", "writer", "wrong", "yard", "yeah", "year", "yes", "yet", "you", "young", "your", "yourself"};
    SDL_Surface* wisielec[] = {wisielec0, wisielec1, wisielec2, wisielec3, wisielec4, wisielec5, wisielec6, wisielec7};
    srand(time(NULL));
    int r, dl, zgadnieteLitery=0, IloscZyc = 7, wpisaneLitery = 0, NrObrazka = 0, niezgadnieteLitery = 0;
    r = rand() % 3;
    char slowo[100], UkryteSlowo[100];

    SDL_Event e;
    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = true;
                //obsługa myszki
            } else if (e.type == SDL_MOUSEBUTTONDOWN) {
                int mouseX, mouseY;
                SDL_GetMouseState(&mouseX, &mouseY);

                //sprawdza czy kliknieto przycisk play
                if (mouseX >= 270 && mouseX <= 504 &&
                    mouseY >= 400 && mouseY <= 484) {
                    playClicked = true;
                }
                // Sprawdza, czy kliknięto przycisk wyjścia
                if (mouseX >= 540 && mouseX <= 774 &&
                    mouseY >= 400 && mouseY <= 484 && playClicked == false) {
                    quit = true;  // Ustawia flagę quit na true, aby przerwać pętlę
                }
                // Sprawdza obszar przycisku mute
                if (mouseX >= 0 && mouseX <= 70 &&
                    mouseY >= 0 && mouseY <= 70) {
                    if (musicplay) {
                        Mix_HaltMusic();
                        musicplay = false;
                    } else {
                        Mix_PlayMusic(backgroundMusic, -1);
                        musicplay = true;
                    }
                }

            }
            else if (e.type == SDL_KEYDOWN && playClicked)
            {

                if (e.key.keysym.sym == SDLK_RETURN && wpisaneLitery == 1) {
                    char Litera = inputText[strlen(inputText)-1];
                    int czy=0;
                    for(int j=0; j<dl; j++)
                    {
                        if(slowo[j]==Litera)
                        {
                            czy=1;
                            zgadnieteLitery++;
                            UkryteSlowo[j]=slowo[j];
                            slowo[j]='_';
                            strncat(inputText, (const char*)&e.key.keysym.sym, 1);
                        }
                    }
                    if(zgadnieteLitery>=dl)
                    {
                        czyWygrales = true;
                    }
                    if(czy == 0)
                    {
                        IloscZyc--;
                        NrObrazka++;
                        niezgadnieteLitery++;
                        if(IloscZyc == 0)
                        {
                            czyPrzegrales = true;
                        }
                    }

                    removeChar(inputText, inputText[0]);

                    for(int i=0;i<strlen(inputText);i++)
                    {
                        removeChar(inputText, inputText[i]);
                    }

                    wpisaneLitery--;


                }

                else if (e.key.keysym.sym == SDLK_BACKSPACE && strlen(inputText) > 0 && wpisaneLitery > 0) {
                    wpisaneLitery--;
                    inputText[strlen(inputText) - 1] = '\0';
                }

                    // Dodaje wprowadzony znak do tekstu (zakładając, że użytkownik wprowadza znaki od spacji do 'z')
                else if (strlen(inputText) < 99 && e.key.keysym.sym > SDLK_SPACE && e.key.keysym.sym <= SDLK_z && wpisaneLitery < 1) {
                    wpisaneLitery++;
                    strncat(inputText, (const char*)&e.key.keysym.sym, 1);
                }


            }
        }




        if (playClicked) {
            SDL_FillRect(surface, NULL, SDL_MapRGB(surface->format, 0, 0, 0));
            SDL_Color textColor = {255, 255, 255}; // Biały kolor tekstu na czarnym tle

            if(czyPrzegrales == false && czyWygrales == false)
            {
                renderText(surface, inputText, 350, 450, font, textColor);

                renderText(surface, UkryteSlowo, 100, 150, font, textColor);

                renderText(surface, "Litera: ", 50, 450, font, textColor);
            }


            if(czyWygrales == true)
            {
                font = TTF_OpenFont("Creepster-Regular.ttf", 150);
                renderText(surface, "YOU WON!", 70, 150, font, textColor);
            }
            if(czyPrzegrales)
            {
                font = TTF_OpenFont("Creepster-Regular.ttf", 150);
                renderText(surface, "YOU LOST!", 70, 150, font, textColor);
            }

            //TU REDEROWANIE OBRAZKA O NUMERZE od 0 do 7 NrObrazka
            SDL_BlitSurface(wisielec[niezgadnieteLitery], NULL, surface, &imageRect);
            //////TEKST randomowy

            dl = strlen(words[r]);
            if(isWypisane == false)
            {
                isWypisane = true;
                for(int i=0; i<dl; i++)
                {
                    slowo[i]=words[r][i];
                    UkryteSlowo[i]='_';
                }
            }

            SDL_Color text2Color = {255, 0, 0}; // czerwony kolor tekstu na czarnym tle
            if(czyWygrales == true || czyPrzegrales == true)
            {
                renderText(surface, words[r], 100, 350, font, text2Color);
            }


        } else {
            renderButton(playButtonSurface, surface, 270, 400, 234, 84);
            renderButton(exitButtonSurface, surface, 540, 400, 234, 84);
            renderButton(muteButtonSurface, surface, 0, 0, 70, 70);
        }

        SDL_UpdateWindowSurface(window);
    }
    //zwalnianie zasobow po skonczeniu programmu (zamykanie wszystkiego itp.)
    TTF_CloseFont(font);
    TTF_Quit();

    SDL_FreeSurface(backgroundSurface);
    SDL_FreeSurface(playButtonSurface);
    SDL_FreeSurface(exitButtonSurface);
    SDL_FreeSurface(muteButtonSurface);

    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
// funkcja do ladowania powierzchni
SDL_Surface* loadSurface(const char* path) {
    SDL_Surface* loadedSurface = SDL_LoadBMP(path);
    if (!loadedSurface) {
        printf("Unable to load image %s! SDL Error: %s\n", path, SDL_GetError());
    }
    return loadedSurface;
}

//funkcja do renderowania przycisku
void renderButton(SDL_Surface* buttonSurface, SDL_Surface* surface, int x, int y, int width, int height) {
    SDL_Rect buttonRect = { x, y, width, height };
    SDL_Rect destRect = { x, y, width, height };

    SDL_BlitScaled(buttonSurface, NULL, surface, &destRect);
}

//Funkcja do renderowania Textu
void renderText(SDL_Surface* surface, const char* text, int x, int y, TTF_Font* font, SDL_Color color) {
    SDL_Surface* textSurface = TTF_RenderText_Solid(font, text, color);
    if (!textSurface) {
        printf("Unable to render text surface! SDL Error: %s\n", TTF_GetError());
    } else {
        SDL_Rect destRect = {x, y, 0, 0};
        SDL_BlitSurface(textSurface, NULL, surface, &destRect);
        SDL_FreeSurface(textSurface);
    }
}

void removeChar(char *str, char garbage) {

    char *src, *dst;
    for (src = dst = str; *src != '\0'; src++) {
        *dst = *src;
        if (*dst != garbage) dst++;
    }
    *dst = '\0';
}