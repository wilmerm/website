/**
 * Copyright (C) 2020 Unolet All rights reserved.
 * Copyright (C) 2020 Wilmer Martinez <wilmermorelmartinez@gmail.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1.  Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 * 2.  Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 * 3.  Neither the name of Unoletsoft SRL, Unolet SRL ("Unolet") nor the names 
 *     of its contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY UNOLET AND ITS CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL UNOLET OR ITS CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
 

/**
 * @name store.js
 * @description Aplicación escrita en Vue para el manejo de la tienda virtual.
 * @version 1.0.0
 * @author Unolet https://www.unolet.com
 * @copyright Unolet
 * @requires (VueJs 3).
 * 
 */



const Store = {
    data() {
        return {
            user: {
                id: 1,
                username: 'Anonimous',
            },
            cart: {
                items: [],
                total: {
                    count: 0,
                    cant: 0,
                    subtotal: 0,
                    tax: 0,
                    total: 0, 
                }
            },
        }
    }
}


//Vue.createApp(Store).mount('#store');