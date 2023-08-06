from pathlib import Path
import os
CSS = """
html {
	scroll-behavior: smooth;
}

body {
	background-color: #111;
	color: #818181;
	font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
	font-size: 20px;
}

body, html {
	height: 100%;
	margin-top: 0;
	margin-bottom: 0;
}
::-webkit-scrollbar {
  width: 0.3em; 
  height: 7px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(150,150,150,0.4);
  outline: 1px solid red;
  border-radius: 50px;
}

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 4px rgba(0,0,0,0.2);
}

.content {
	height: 100%;
	max-width: 80em;
	margin: auto;
	font-size: large;
	display: grid;
	grid-template-columns: 1fr 3fr;
}

/* The sidebar menu */
.sidenav {
	height: 100%;
	grid-column: 1;
	background-color: #222; /* Black */
	overflow-x: hidden; /* Disable horizontal scroll */
	overflow-y: auto;
}

/* The navigation menu links */
.sidenav a {
	padding: 6px 8px 6px 16px;
	text-decoration: none;
	color: #818181;
	display: block;
}

/* When you mouse over the navigation links, change their color */
.sidenav a:hover {
	color: #f1f1f1;
}

/* Style page content */
.article {
	height: 100%;
	grid-column: 2;
	overflow-y: auto;
	padding: 0px 10px;
	scroll-behavior: smooth;
}

	/* On smaller screens, where height is less than 450px, change the style of the sidebar (less padding and a smaller font size) */
	@media screen and (max-height: 450px) {
		.sidenav {padding-top: 15px;}
		.sidenav a {font-size: 18px;}
	}
	p {
		line-height: 1.6;
	}

"""


def get_css():
    """
    gets file from $HOME/.config/wikireader/layout.css or saves default
    and then reads it
    """
    config_dir = Path(os.environ['HOME']) / '.config/wikireader'
    if not config_dir.exists():
        config_dir.mkdir()
    css_file =  config_dir / 'layout.css'
    if not css_file.exists():
        css_file.write_text(CSS)
    return css_file.read_text()

