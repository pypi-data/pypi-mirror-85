#ifndef NUMEXPR_REAL_FUNCTIONS_HPP
#define NUMEXPR_REAL_FUNCTIONS_HPP

/*********************************************************************
  Numexpr - Fast numerical array expression evaluator for NumPy.

      License: BSD
      Author:  See AUTHORS.txt

  See LICENSE.txt for details about copyright and rights to use.
**********************************************************************/
/*
 * Useful constants
 */

#define NPY_E         2.718281828459045235360287471352662498  /* e */
#define NPY_LOG2E     1.442695040888963407359924681001892137  /* log_2 e */
#define NPY_LOG10E    0.434294481903251827651128918916605082  /* log_10 e */
#define NPY_LOGE2     0.693147180559945309417232121458176568  /* log_e 2 */
#define NPY_LOGE10    2.302585092994045684017991454684364208  /* log_e 10 */
#define NPY_PI        3.141592653589793238462643383279502884  /* pi */
#define NPY_PI_2      1.570796326794896619231321691639751442  /* pi/2 */
#define NPY_PI_4      0.785398163397448309615660845819875721  /* pi/4 */
#define NPY_1_PI      0.318309886183790671537767526745028724  /* 1/pi */
#define NPY_2_PI      0.636619772367581343075535053490057448  /* 2/pi */
#define NPY_EULER     0.577215664901532860606512090082402431  /* Euler constant */
#define NPY_SQRT2     1.414213562373095048801688724209698079  /* sqrt(2) */
#define NPY_SQRT1_2   0.707106781186547524400844362104849039  /* 1/sqrt(2) */

#define NPY_Ef        2.718281828459045235360287471352662498F /* e */
#define NPY_LOG2Ef    1.442695040888963407359924681001892137F /* log_2 e */
#define NPY_LOG10Ef   0.434294481903251827651128918916605082F /* log_10 e */
#define NPY_LOGE2f    0.693147180559945309417232121458176568F /* log_e 2 */
#define NPY_LOGE10f   2.302585092994045684017991454684364208F /* log_e 10 */
#define NPY_PIf       3.141592653589793238462643383279502884F /* pi */
#define NPY_PI_2f     1.570796326794896619231321691639751442F /* pi/2 */
#define NPY_PI_4f     0.785398163397448309615660845819875721F /* pi/4 */
#define NPY_1_PIf     0.318309886183790671537767526745028724F /* 1/pi */
#define NPY_2_PIf     0.636619772367581343075535053490057448F /* 2/pi */
#define NPY_EULERf    0.577215664901532860606512090082402431F /* Euler constant */
#define NPY_SQRT2f    1.414213562373095048801688724209698079F /* sqrt(2) */
#define NPY_SQRT1_2f  0.707106781186547524400844362104849039F /* 1/sqrt(2) */

#define NPY_El        2.718281828459045235360287471352662498L /* e */
#define NPY_LOG2El    1.442695040888963407359924681001892137L /* log_2 e */
#define NPY_LOG10El   0.434294481903251827651128918916605082L /* log_10 e */
#define NPY_LOGE2l    0.693147180559945309417232121458176568L /* log_e 2 */
#define NPY_LOGE10l   2.302585092994045684017991454684364208L /* log_e 10 */
#define NPY_PIl       3.141592653589793238462643383279502884L /* pi */
#define NPY_PI_2l     1.570796326794896619231321691639751442L /* pi/2 */
#define NPY_PI_4l     0.785398163397448309615660845819875721L /* pi/4 */
#define NPY_1_PIl     0.318309886183790671537767526745028724L /* 1/pi */
#define NPY_2_PIl     0.636619772367581343075535053490057448L /* 2/pi */
#define NPY_EULERl    0.577215664901532860606512090082402431L /* Euler constant */
#define NPY_SQRT2l    1.414213562373095048801688724209698079L /* sqrt(2) */
#define NPY_SQRT1_2l  0.707106781186547524400844362104849039L /* 1/sqrt(2) */

// This integer power is a use case where templates would result in much less code.
static inline void
_inline_ipow(npy_uint8 base, npy_uint8 exponent, npy_uint8 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_uint8 x = base;     // Don't modify input args
    npy_uint8 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_int8 base, npy_int8 exponent, npy_int8 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_int8 x = base;     // Don't modify input args
    npy_int8 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_uint16 base, npy_uint16 exponent, npy_uint16 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_uint16 x = base;     // Don't modify input args
    npy_uint16 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_int16 base, npy_int16 exponent, npy_int16 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_int16 x = base;     // Don't modify input args
    npy_int16 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_uint32 base, npy_uint32 exponent, npy_uint32 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_uint32 x = base;     // Don't modify input args
    npy_uint32 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_int32 base, npy_int32 exponent, npy_int32 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_int32 x = base;     // Don't modify input args
    npy_int32 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_uint64 base, npy_uint64 exponent, npy_uint64 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_uint64 x = base;     // Don't modify input args
    npy_uint64 n = exponent;
    while(n) {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    }
}

static inline void
_inline_ipow(npy_int64 base, npy_int64 exponent, npy_int64 &result) {
    result = 1;
    if (exponent <= 0) {
        return;
    }
    npy_int64 x = base;     // Don't modify input args
    npy_int64 n = exponent;
    do {
        if (n & 1) 
            result *= x;
        n >>= 1;
        x *= x;
    } while(n);
}

static void
nr_int_pow(npy_intp n, npy_uint8 *a, npy_intp sb1, npy_uint8 *b, npy_intp sb2, npy_uint8 *r) {
    if( sb1 == sizeof(npy_uint8) && sb2 == sizeof(npy_uint8) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_uint8);
        sb2 /= sizeof(npy_uint8);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_int8 *a, npy_intp sb1, npy_int8 *b, npy_intp sb2, npy_int8 *r) {
    if( sb1 == sizeof(npy_int8) && sb2 == sizeof(npy_int8) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_int8);
        sb2 /= sizeof(npy_int8);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_uint16 *a, npy_intp sb1, npy_uint16 *b, npy_intp sb2, npy_uint16 *r) {
    if( sb1 == sizeof(npy_uint16) && sb2 == sizeof(npy_uint16) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_uint16);
        sb2 /= sizeof(npy_uint16);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_int16 *a, npy_intp sb1, npy_int16 *b, npy_intp sb2, npy_int16 *r) {
    if( sb1 == sizeof(npy_int16) && sb2 == sizeof(npy_int16) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_int16);
        sb2 /= sizeof(npy_int16);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_uint32 *a, npy_intp sb1, npy_uint32 *b, npy_intp sb2, npy_uint32 *r) {
    if( sb1 == sizeof(npy_uint32) && sb2 == sizeof(npy_uint32) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_uint32);
        sb2 /= sizeof(npy_uint32);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_int32 *a, npy_intp sb1, npy_int32 *b, npy_intp sb2, npy_int32 *r) {
    if( sb1 == sizeof(npy_int32) && sb2 == sizeof(npy_int32) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_int32);
        sb2 /= sizeof(npy_int32);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_uint64 *a, npy_intp sb1, npy_uint64 *b, npy_intp sb2, npy_uint64 *r) {
    if( sb1 == sizeof(npy_uint64) && sb2 == sizeof(npy_uint64) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_uint64);
        sb2 /= sizeof(npy_uint64);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

static void
nr_int_pow(npy_intp n, npy_int64 *a, npy_intp sb1, npy_int64 *b, npy_intp sb2, npy_int64 *r) {
    if( sb1 == sizeof(npy_int64) && sb2 == sizeof(npy_int64) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I], b[I], r[I]);
        }
    }
    else {
        sb1 /= sizeof(npy_int64);
        sb2 /= sizeof(npy_int64);
        for( npy_intp I = 0; I < n; I++ ) {
            _inline_ipow(a[I*sb1], b[I*sb2], r[I]);
        }
    }
}

// logaddexp
static void
nr_logaddexp( npy_intp n, npy_float32 *a, npy_intp sb1, npy_float32 *b, npy_intp sb2, npy_float32 *r )
{
    npy_float32 diff;
    if( sb1 == sizeof(npy_float32) && sb2 == sizeof(npy_float32) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            if( a[I] == b[I]) {
                r[I] = a[I] + (npy_float32)NPY_LOGE2;
            }
            else {
                diff = a[I] - b[I];
                if(diff > 0.0f) {
                    r[I] = a[I] + log1p(exp(-diff));
                }
                else if(diff <= 0.0f) {
                    r[I] = b[I] + log1p(exp(diff));
                }
                else { // NaNs
                    r[I] = diff;
                }
            }
        }
    }
    else {
        sb1 /= sizeof(npy_float32);
        sb2 /= sizeof(npy_float32);
        for( npy_intp I = 0; I < n; I++ ) {
            if( a[I*sb1] == b[I*sb2]) {
                r[I] = a[I*sb1] + (npy_float32)NPY_LOGE2;
            }
            else {
                diff = a[I*sb1] - b[I*sb2];
                if(diff > 0.0f) {
                    r[I] = a[I*sb1] + log1p(exp(-diff));
                }
                else if(diff <= 0.0f) {
                    r[I] = b[I*sb2] + log1p(exp(diff));
                }
                else { // NaNs
                    r[I] = diff;
                }
            }
        }
    }
}
  
static void
nr_logaddexp( npy_intp n, npy_float64 *a, npy_intp sb1, npy_float64 *b, npy_intp sb2, npy_float64 *r )
{
    npy_float64 diff;
    if( sb1 == sizeof(npy_float64) && sb2 == sizeof(npy_float64) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            if( a[I] == b[I]) {
                r[I] = a[I] + NPY_LOGE2;
            } 
            else {
                diff = a[I] - b[I];
                if(diff > 0.0f) {
                    r[I] = a[I] + log1p(exp(-diff));
                } 
                else if(diff <= 0.0f) {
                    r[I] = b[I] + log1p(exp(diff));
                } 
                else { // NaNs
                    r[I] = diff;
                }
            }
        }
    }
    else {
        sb1 /= sizeof(npy_float64);
        sb2 /= sizeof(npy_float64);
        for( npy_intp I = 0; I < n; I++ ) {
            if( a[I*sb1] == b[I*sb2]) {
                r[I] = a[I*sb1] + NPY_LOGE2;
            } else {
                diff = a[I*sb1] - b[I*sb2];
                if(diff > 0.0f) {
                    r[I] = a[I*sb1] + log1p(exp(-diff));
                } else if(diff <= 0.0f) {
                    r[I] = b[I*sb2] + log1p(exp(diff));
                } else { // NaNs
                    r[I] = diff;
                }
            }
        }
    }
}

static void
nr_heaviside( npy_intp n, npy_float32 *a, npy_intp sb1, npy_float32 *b, npy_intp sb2, npy_float32 *r )
{
    
    if( sb1 == sizeof(npy_float32) && sb2 == sizeof(npy_float32) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            if(isnan(a[I])) {
                r[I] = a[I];
            } 
            else if (a[I] == (npy_float32)0.0) {
                r[I] = b[I];
            } 
            else if (a[I] < (npy_float32)0.0) {
                r[I] = (npy_float32)0.0;
            } else {
                r[I] = (npy_float32)1.0;
            }
        }
    }
    else {
        sb1 /= sizeof(npy_float32);
        sb2 /= sizeof(npy_float32);
        for( npy_intp I = 0; I < n; I++ ) {
            if(isnan(a[I*sb1])) {
                r[I] = a[I*sb1];
            } 
            else if (a[I*sb1] == (npy_float32)0.0) {
                r[I] = b[I*sb2];
            } 
            else if (a[I*sb1] < (npy_float32)0.0) {
                r[I] = (npy_float32)0.0;
            } else {
                r[I] = (npy_float32)1.0;
            }
        }
    }
}

static void
nr_heaviside( npy_intp n, npy_float64 *a, npy_intp sb1, npy_float64 *b, npy_intp sb2, npy_float64 *r )
{
    
    if( sb1 == sizeof(npy_float64) && sb2 == sizeof(npy_float64) ) { // Aligned
        for( npy_intp I = 0; I < n; I++ ) {
            if(isnan(a[I])) {
                r[I] = a[I];
            } 
            else if (a[I] == (npy_float64)0.0) {
                r[I] = b[I];
            } 
            else if (a[I] < (npy_float64)0.0) {
                r[I] = (npy_float64)0.0;
            } else {
                r[I] = (npy_float64)1.0;
            }
        }
    }
    else {
        sb1 /= sizeof(npy_float64);
        sb2 /= sizeof(npy_float64);
        for( npy_intp I = 0; I < n; I++ ) {
            if(isnan(a[I*sb1])) {
                r[I] = a[I*sb1];
            } 
            else if (a[I*sb1] == (npy_float64)0.0) {
                r[I] = b[I*sb2];
            } 
            else if (a[I*sb1] < (npy_float64)0.0) {
                r[I] = (npy_float64)0.0;
            } else {
                r[I] = (npy_float64)1.0;
            }
        }
    }
}

#endif // NUMEXPR_REAL_FUNCTIONS_HPP