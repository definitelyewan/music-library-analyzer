#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <id3v1/id3v1.h>
#include <id3v2/id3v2.h>
#include <id3v2/id3v2Frame.h>
#include <id3dev.h>

void removeChar(char *str, char ch) {
    char *src = str;
    char *dst = str;
    while (*src) {
        if (*src != ch) {
            *dst++ = *src;
        }
        src++;
    }
    *dst = '\0';
}

void replaceChar(char *str, char ch, char newCh) {
    
    if(str == NULL){
        return;
    }

    char *src = str;
    while (*src) {
        if (*src == ch) {
            *src = newCh;
        }
        src++;
    }
}

void removeSpecialChars(char *str){
    
    if(str == NULL){
        return;
    }
    
    removeChar(str, ',');
    removeChar(str, '\n');
    removeChar(str, '\t');
    removeChar(str, '\r');
}

void specialConsiderations(char *str){
    
    if(str == NULL){
        return;

    }

    if(strlen(str) >= strlen("Tyler/ The Creator")){
        char *substr = strstr(str, "Tyler/ The Creator");
        if(substr != NULL){
            memmove(substr + 5, substr + 6, strlen(substr + 6) + 1);
        }
    }

    if(strlen(str) >= strlen("Mandy/ Indiana")){
        char *substr = strstr(str, "Mandy/ Indiana");
        if(substr != NULL){
            memmove(substr + 5, substr + 6, strlen(substr + 6) + 1); // Shift characters left by one
        }

    }

    if(strlen(str) >= strlen("Earth, Wind , Fire")){
        char *substr = strstr(str, "Earth/ Wind / Fire");
        if(substr != NULL){
            for(int i = 0; substr[i] != '\0'; i++){
                if(substr[i] == '/'){
                    memmove(substr + i, substr + i + 1, strlen(substr + i));
                    i--;
                }
            }
        }
    }

    if(strlen(str) >= strlen("Black Country/ New Road")){
        char *substr = strstr(str, "Black Country/ New Road");
        if(substr != NULL){
            substr[13] = ' ';
            memmove(substr + 14, substr + 15, strlen(substr + 15) + 1);
        }
    }

    if(strlen(str) >= strlen("R/B")){
        char *substr = str;
        while((substr = strstr(substr, "R/B")) != NULL){
            substr[1] = '&';
            substr += 2;
        }
    }

}


int main(int argc, char *argv[]){

    if(argc < 2){
        printf("[ERROR] : no argv[1]\n");
        return EXIT_FAILURE;
    }

    FILE *f = NULL;
    FILE *csv = NULL;
    size_t sz = 0;
    size_t stringCount = 0;
    char *fileContent = NULL;
    char *index = NULL;
    char **strings = NULL;

    f = fopen(argv[1], "r");

    if(f == NULL){
        printf("[ERROR] : File not found!\n");
        return EXIT_FAILURE;
    }

    // file size
    fseek(f, 0, SEEK_END);
    sz = ftell(f);
    fseek(f, 0, SEEK_SET);

    // read file
    fileContent = calloc(sz, sizeof(char));
    fread(fileContent, sizeof(char), sz, f);

    // create new strings
    for(size_t i = 0; i < sz; i++){
        if(fileContent[i] == '\n'){
            fileContent[i] = '\0';
            stringCount++;
        }
    }

    // create a 2d array for strings
    strings = calloc(stringCount, sizeof(char*));

    index = fileContent;

    size_t c = 0;
    while(c < stringCount){
        int len = 0;
        len = strlen(index);

        strings[c] = calloc(len + 1, sizeof(char));
        strcpy(strings[c], index);
        index += len + 1;
        c++;
    }

    // create a file for a csv
    csv = fopen("build/metadata.csv", "w");

    if(csv == NULL){
        printf("[ERROR] : Could not create metadata.csv\n");
        
        for(size_t i = 0; i < stringCount; i++){
            free(strings[i]);
        }
        free(strings);
        
        return EXIT_FAILURE;
    }


    fwrite("ID3v1,ID3v2_ver,Title,Artist,Album_Artist,Album,Year,Genre,Track,Composer,Disc,Lyrics,Comment,Pictures\n", sizeof(char), 103, csv);


    for(size_t i = 0; i < stringCount; i++){

        // printf("[*] Reading %s for metadata\n", strings[i]);


        ID3 *id3 = id3FromFile(strings[i]);

        bool hasId3v1 = false;
        int id3v2Version = 0;
        char *title = NULL;
        char *artist = NULL;
        char *albumArtist = NULL;
        char *album = NULL;
        char *year = NULL;
        char *genre = NULL;
        char *track = NULL;
        char *composer = NULL;
        char *disc = NULL;
        char *lyrics = NULL;
        char *comment = NULL;
        int pictures = 0;
        char *line = NULL;
        size_t memCount = 0;
        Id3v2Frame *frame = NULL;
        ListIter frames = {0};
        


        if(id3->id3v1 != NULL){
            hasId3v1 = true;
        }

        if(id3->id3v2 != NULL){
            id3v2Version = id3->id3v2->header->majorVersion;
        }


        title = id3ReadTitle(id3);
        artist = id3ReadArtist(id3);
        albumArtist = id3ReadAlbumArtist(id3);
        album = id3ReadAlbum(id3);
        year = id3ReadYear(id3);
        genre = id3ReadGenre(id3);
        track = id3ReadTrack(id3);
        composer = id3ReadComposer(id3);
        disc = id3ReadDisc(id3);
        lyrics = id3ReadLyrics(id3);
        comment = id3ReadComment(id3);
        
        frames = id3v2CreateFrameTraverser(id3->id3v2);
        
        while((frame = id3v2FrameTraverse(&frames)) != NULL){
            if(memcmp(frame->header->id, "APIC", ID3V2_FRAME_ID_MAX_SIZE) == 0 || memcmp(frame->header->id, "PIC", ID3V2_FRAME_ID_MAX_SIZE) == 0){
                pictures++;
            }
        }

        /**
         * the format: 
         * snog name (ft. name, name2 & name 3)
         *           ^ issue!
         * is possible so , and & are going to be linted to help me out later with R.
         */

        if(title != NULL){
            for(int j = 0; j < strlen(title); j++){
                if(title[j] == '(' || title[j] == '['){
                    replaceChar(title + j, ',', '/');
                    replaceChar(title + j, '&', '/');
                    specialConsiderations(title + j);
                    break;
                }

            }
            specialConsiderations(title);
            removeSpecialChars(title);
        }


        replaceChar(artist, ',', '/');
        replaceChar(artist, '&', '/');
        specialConsiderations(artist);
        removeSpecialChars(artist);


        replaceChar(albumArtist, ',', '/');
        replaceChar(artist, '&', '/');
        specialConsiderations(albumArtist);
        removeSpecialChars(albumArtist);


        removeSpecialChars(album);

        removeSpecialChars(year);


        /**
         * format:
         *  (n)
         * is possible so this will need to be fixed for R
         * 
         */
        replaceChar(genre, ',', '/');
        replaceChar(genre, '&', '/');
        specialConsiderations(genre);
        removeSpecialChars(genre);

        if(genre != NULL){
            if(genre[0] == '(' && genre[strlen(genre) - 1] == ')'){
                if(genre != NULL){
                    if(genre[0] == '(' && genre[strlen(genre) - 1] == ')'){
                        memmove(genre, genre + 1, strlen(genre) - 2);
                        genre[strlen(genre) - 1] = '\0';
                        int g = atoi(genre);
                        printf("[*]->[%d] which is [%s]\n", g,id3v1GenreFromTable(g));
                        free(genre);
                        genre = calloc(strlen(id3v1GenreFromTable(g)) + 1, sizeof(char));
                        strcpy(genre, id3v1GenreFromTable(g));


                    }
                }
            }
        }

        printf("[*]->[%s]\n", genre);

        removeSpecialChars(track);

        replaceChar(composer, ',', '/');
        replaceChar(composer, ',', '&');
        specialConsiderations(composer);
        removeSpecialChars(composer);
        
        removeSpecialChars(disc);

        replaceChar(lyrics, '\n', ' ');
        removeSpecialChars(lyrics);

        replaceChar(comment, ',', '/');
        removeSpecialChars(comment);


        memCount += snprintf(NULL, 0,
                            "%s,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d\n",
                            hasId3v1 ? "Yes" : "No",
                            id3v2Version,
                            title == NULL ? "" : title,
                            artist == NULL ? "" : artist,
                            albumArtist == NULL ? "" : albumArtist,
                            album == NULL ? "" : album,
                            year == NULL ? "" : year,
                            genre == NULL ? "" : genre,
                            track == NULL ? "" : track,
                            composer == NULL ? "" : composer,
                            disc == NULL ? "" : disc,
                            lyrics == NULL ? "" : lyrics,
                            comment == NULL ? "" : comment,
                            pictures
                            ); 
                            
        line = calloc(memCount + 1, sizeof(char));

        snprintf(line, memCount + 1,
                "%s,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d\n",
                hasId3v1 ? "Yes" : "No",
                id3v2Version,
                title == NULL ? "" : title,
                artist == NULL ? "" : artist,
                albumArtist == NULL ? "" : albumArtist,
                album == NULL ? "" : album,
                year == NULL ? "" : year,
                genre == NULL ? "" : genre,
                track == NULL ? "" : track,
                composer == NULL ? "" : composer,
                disc == NULL ? "" : disc,
                lyrics == NULL ? "" : lyrics,
                comment == NULL ? "" : comment,
                pictures
                );
        
        fwrite(line, sizeof(char), memCount, csv);


        if(title != NULL){
            free(title);
        }
        
        if(artist != NULL){
            free(artist);
        }
        
        if(albumArtist != NULL){
            free(albumArtist);
        }
        
        if(album != NULL){
            free(album);
        }
        
        if(year != NULL){
            free(year);
        }
        
        if(genre != NULL){
            free(genre);
        }
        
        if(track != NULL){
            free(track);
        }
        
        if(composer != NULL){
            free(composer);
        }
        
        if(disc != NULL){
            free(disc);
        }
        
        if(lyrics != NULL){
            free(lyrics);
        }
        
        if(comment != NULL){
            free(comment);
        }


        free(line);
        id3Destroy(&id3);
        free(strings[i]);
    }
    fclose(csv);
    free(strings);
    free(fileContent);
    fclose(f);
    return EXIT_SUCCESS;
}