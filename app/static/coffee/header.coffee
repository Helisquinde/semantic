class Header

    #a list to be passed to the link generator function
    links: [
        {title: "Home", url: "/home"}
        {title: "Group Browse", url: "/gbrowse"}
        {title: "Group Analyses", url: "/groups"}
        {title: "VF and AMR", url: "/factors"}
    ]

    controller: ->

    view: ->
        m("div", {class:'container-fluid'}, [
            m("nav", {class:'navbar navbar-default navbar-fixed-top', role:'navigation'}, [
                m("div", {class:'navbar-header'}, [
                    m("a", {class:"navbar-brand", href:"/home", config:m.route}, "SuperPhy")
                ])
                m("ul", {class:'nav navbar-nav'}, [
                    m("li", m("a", {href: link.url, config:m.route}, link.title)) for link in @links
                    m("li", {class:"dropdown"}, [
                        m("a", {href:"", role:"button", class:"dropdown-toggle", 'data-toggle':"dropdown"}, "My Data", [
                            m("b", {class:"caret"})
                        ])
                    ])
                ])
            ])
        ])

header = new Header()