/* common.h - Header for all common functions in common.c */

/*
    libzint - the open source barcode library
    Copyright (C) 2009 - 2020 Robin Stuart <rstuart114@gmail.com>

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the project nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
 */
/* vim: set ts=4 sw=4 et : */

/* Used in some logic */
#ifndef __COMMON_H
#define __COMMON_H

#ifndef FALSE
#define FALSE   0
#endif

#ifndef TRUE
#define TRUE    1
#endif

/* The most commonly used set */
#define NEON   "0123456789"

#include "zint.h"
#include <stdlib.h>
#include <string.h>

/* Helpers to cast away char pointer signedness */
#define ustrlen(source) strlen((const char *) (source))
#define ustrcpy(target, source) strcpy((char *) (target), (const char *) (source))
#define ustrcat(target, source) strcat((char *) (target), (const char *) (source))

#if defined(__GNUC__) && !defined(_WIN32) && !defined(ZINT_TEST)
#define INTERNAL __attribute__ ((visibility ("hidden")))
#else
#define INTERNAL
#endif

#if defined(ZINT_TEST)
#define STATIC_UNLESS_ZINT_TEST
#else
#define STATIC_UNLESS_ZINT_TEST static
#endif

#define COMMON_INLINE   1

#ifdef COMMON_INLINE
/* Return true (1) if a module is dark/black, otherwise false (0) */
#define module_is_set(s, y, x) (((s)->encoded_data[(y)][(x) >> 3] >> ((x) & 0x07)) & 1)

/* Set a module to dark/black */
#define set_module(s, y, x) do { (s)->encoded_data[(y)][(x) >> 3] |= 1 << ((x) & 0x07); } while (0)

/* Return true (1-8) if a module is colour, otherwise false (0) */
#define module_colour_is_set(s, y, x) ((s)->encoded_data[(y)][(x)])

/* Set a module to a colour */
#define set_module_colour(s, y, x, c) do { (s)->encoded_data[(y)][(x)] = (c); } while (0)
#endif

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

    INTERNAL int ctoi(const char source);
    INTERNAL char itoc(const int source);
    INTERNAL void to_upper(unsigned char source[]);
    INTERNAL int is_sane(const char test_string[], const unsigned char source[], const size_t length);
    INTERNAL void lookup(const char set_string[], const char *table[], const char data, char dest[]);
    INTERNAL void bin_append(const int arg, const int length, char *binary);
    INTERNAL int bin_append_posn(const int arg, const int length, char *binary, int posn);
    INTERNAL int posn(const char set_string[], const char data);
    #ifndef COMMON_INLINE
    INTERNAL int module_is_set(const struct zint_symbol *symbol, const int y_coord, const int x_coord);
    INTERNAL void set_module(struct zint_symbol *symbol, const int y_coord, const int x_coord);
    INTERNAL int module_colour_is_set(const struct zint_symbol *symbol, const int y_coord, const int x_coord);
    INTERNAL void set_module_colour(struct zint_symbol *symbol, const int y_coord, const int x_coord, const int colour);
    #endif
    INTERNAL void unset_module(struct zint_symbol *symbol, const int y_coord, const int x_coord);
    INTERNAL void expand(struct zint_symbol *symbol, const char data[]);
    INTERNAL int is_stackable(const int symbology);
    INTERNAL int is_extendable(const int symbology);
    INTERNAL int is_composite(const int symbology);
    INTERNAL int istwodigits(const unsigned char source[], const int length, const int position);
    INTERNAL unsigned int decode_utf8(unsigned int *state, unsigned int *codep, const unsigned char byte);
    INTERNAL int utf8_to_unicode(struct zint_symbol *symbol, const unsigned char source[], unsigned int vals[],
                    size_t *length, int disallow_4byte);
    INTERNAL void set_minimum_height(struct zint_symbol *symbol, const int min_height);

    typedef unsigned int *(*pn_head_costs)(unsigned int state[]);
    typedef unsigned int (*pn_switch_cost)(unsigned int state[], const int k, const int j);
    typedef unsigned int (*pn_eod_cost)(unsigned int state[], const int k);
    typedef void (*pn_cur_cost)(unsigned int state[], const unsigned int data[], const size_t length, const int i,
                                char *char_modes, unsigned int prev_costs[], unsigned int cur_costs[]);
    INTERNAL void pn_define_mode(char *mode, const unsigned int data[], const size_t length, const int debug,
                    unsigned int state[], const char mode_types[], const int num_modes,
                    pn_head_costs head_costs, pn_switch_cost switch_cost, pn_eod_cost eod_cost, pn_cur_cost cur_cost);
    
    INTERNAL int colour_to_red(int colour);
    INTERNAL int colour_to_green(int colour);
    INTERNAL int colour_to_blue(int colour);

    #ifdef ZINT_TEST
    void debug_test_codeword_dump(struct zint_symbol *symbol, unsigned char *codewords, int length);
    void debug_test_codeword_dump_int(struct zint_symbol *symbol, int *codewords, int length);
    #endif

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* __COMMON_H */
