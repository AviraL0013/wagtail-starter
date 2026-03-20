from django.utils.html import format_html
from wagtail import hooks

@hooks.register("insert_global_admin_css")
def add_shepherd_css():
    return format_html("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/shepherd.js@11.2.0/dist/css/shepherd.css"/>
        <style>
            .shepherd-element {{
                max-width: 380px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.18);
                border: none;
            }}
            .shepherd-content {{
                border-radius: 12px;
                padding: 0;
                overflow: hidden;
            }}
            .shepherd-header {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                padding: 18px 22px 14px;
                border-radius: 12px 12px 0 0;
            }}
            .shepherd-title {{
                color: #000000 !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                letter-spacing: 0.2px;
            }}
            .shepherd-cancel-icon {{
                color: rgba(255,255,255,0.8) !important;
                font-size: 22px !important;
            }}
            .shepherd-cancel-icon:hover {{
                color: #ffffff !important;
            }}
            .shepherd-text {{
                padding: 16px 22px;
                font-size: 14px;
                line-height: 1.6;
                color: #e2e8f0;
                background: #0f3460;
            }}
            .shepherd-footer {{
                padding: 12px 22px 16px;
                background: #16213e;
border-top: 1px solid #1a4fa0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-radius: 0 0 12px 12px;
            }}
            .shepherd-button {{
                border-radius: 8px !important;
                padding: 8px 20px !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                border: none !important;
                cursor: pointer !important;
                transition: all 0.2s !important;
            }}
            .shepherd-button-primary {{
                background: #2c7be5 !important;
                color: #ffffff !important;
            }}
            .shepherd-button-primary:hover {{
                background: #1a4fa0 !important;
                transform: translateY(-1px);
            }}
            .shepherd-button-secondary {{
                background: #e2e8f0 !important;
                color: #4a5568 !important;
            }}
            .shepherd-button-secondary:hover {{
                background: #cbd5e0 !important;
            }}
            .shepherd-arrow::before {{
                background: #2c7be5 !important;
            }}
            .tour-step-counter {{
                font-size: 12px;
                color: #a0aec0;
                font-weight: 500;
            }}
            .tour-emoji {{
                font-size: 28px;
                display: block;
                margin-bottom: 8px;
            }}
        </style>
    """)


@hooks.register("insert_global_admin_js")
def add_tour_js():
    return format_html("""
        <script src="https://cdn.jsdelivr.net/npm/shepherd.js@11.2.0/dist/js/shepherd.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.location.pathname !== '/admin/') return;
            if (localStorage.getItem('wagtail_news_tour_done')) return;

            const tour = new Shepherd.Tour({{
                useModalOverlay: false,
                defaultStepOptions: {{
                    cancelIcon: {{ enabled: true }},
                    scrollTo: {{ behavior: 'smooth', block: 'center' }},
                    popperOptions: {{
                        modifiers: [{{ name: 'offset', options: {{ offset: [0, 16] }} }}]
                    }}
                }}
            }});

            const steps = [
                {{
                    id: 'welcome',
                    title: '👋 Welcome to your News Site!',
                    text: 'This is the Wagtail admin - your content management dashboard. Let us show you around in 4 quick steps.',
                    buttons: [
                        {{
                            text: 'Skip tour',
                            classes: 'shepherd-button-secondary',
                            action: function() {{
                                localStorage.setItem('wagtail_news_tour_done', 'true');
                                tour.complete();
                            }}
                        }},
                        {{ text: 'Let\\'s go →', classes: 'shepherd-button-primary', action: tour.next }}
                    ]
                }},
                {{
                    id: 'pages',
                    title: '📄 Pages - Your Content',
                    text: 'Everything you publish lives here. Your homepage, news articles, and standard pages are all managed from Pages.',
                    attachTo: {{ element: '[href="/admin/pages/"]', on: 'right' }},
                    buttons: [
                        {{ text: '← Back', classes: 'shepherd-button-secondary', action: tour.back }},
                        {{ text: 'Next →', classes: 'shepherd-button-primary', action: tour.next }}
                    ]
                }},
                {{
                    id: 'snippets',
                    title: '✂️ Snippets - Reusable Content',
                    text: 'Authors and Topics are stored here as Snippets. Create an author once and attach them to any number of articles.',
                    attachTo: {{ element: '[href="/admin/snippets/"]', on: 'right' }},
                    buttons: [
                        {{ text: '← Back', classes: 'shepherd-button-secondary', action: tour.back }},
                        {{ text: 'Next →', classes: 'shepherd-button-primary', action: tour.next }}
                    ]
                }},
                {{
                    id: 'search',
                    title: '🔍 Promoted Search Results',
                    text: 'Pin specific articles to the top of search results for any keyword. A powerful editorial tool that most newcomers never discover.',
                    attachTo: {{ element: '[href="/admin/search/"]', on: 'right' }},
                    buttons: [
                        {{ text: '← Back', classes: 'shepherd-button-secondary', action: tour.back }},
                        {{
                            text: '🎉 Done!',
                            classes: 'shepherd-button-primary',
                            action: function() {{
                                localStorage.setItem('wagtail_news_tour_done', 'true');
                                tour.complete();
                            }}
                        }}
                    ]
                }}
            ];

            steps.forEach(step => tour.addStep(step));
            
            setTimeout(() => tour.start(), 800);
        }});
        </script>
    """)