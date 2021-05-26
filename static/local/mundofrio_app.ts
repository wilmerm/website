





const App = {
    data() {
        return {
            current_page: {
                title: "¡Próximamente!",
            },
            site: SITE,
            settings: {
                navbar: {
                    active: false,
                },
                cover: {
                    active: true,
                    image: SITE.logo,
                },
                body: {
                }
            }
        }
    }
}

const app = Vue.createApp(App);

// Add here components...

app.mount("#app");