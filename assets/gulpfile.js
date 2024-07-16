'use strict';

/*
    Verificar: 

    Node
    v20.13.1

    Gulp
    CLI version: 3.0.0
    Local version: 5.0.0

*/

const { src, dest, watch, parallel, series } = require('gulp');

const sass = require('gulp-sass')(require('sass'));
const sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
// js
var uglify = require('gulp-uglify');                // apenas para o Javascript

// css
const cleanCSS = require('gulp-clean-css');
const path = require('path');
const autoprefixer = require('autoprefixer')
const postcss = require('gulp-postcss')
// img


//////////////////////////////////////////////////////////////////////////////////////////

// sass
function styles() {
    return src('sass/estilos.scss')    
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(postcss([ autoprefixer() ]))
        .pipe(cleanCSS())
        .pipe(sourcemaps.write('.'))
        .pipe(dest('../lib/css'));
};
// Lib CSS
function bibliotecasCSS() {
    return src(['node_modules/bootstrap/dist/css/bootstrap.css', 'node_modules/owl.carousel/dist/assets/owl.carousel.css'])
        .pipe(concat('biblioteca.css'))
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(cleanCSS())
        .pipe(sourcemaps.write('.'))
        .pipe(dest('../lib/css'));
};

// fontes
function fontes() {
    return src(['fontes/*.ttf', 'fontes/*.eot', 'fontes/*.woff'])
        .pipe(dest('../lib/fontes/'));
}
function fontStyles() {
    return src('fontes/stylesheet.css')    
        .pipe(concat('fontes.css'))
        .pipe(sourcemaps.init())
        .pipe(cleanCSS())
        .pipe(sourcemaps.write('.'))
        .pipe(dest('../lib/css'));
};

// exports from functions
exports.styles = styles;
exports.bibliotecasCSS = bibliotecasCSS;
exports.fontes = fontes;
exports.fontStyles = fontStyles;

//////////////////////////////////////////////////////////////////////////////////////////

function libJavascript() {
	return src( 'js/lib/**/*.js', {sourcemaps: true})
        
        .pipe(uglify())
        
		.pipe(dest('../lib/js'));
}

function funcoes() {
	return src( 'js/funcoes/**/*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(concat('main.min.js'))
        .pipe(sourcemaps.write('.'))
		.pipe(dest('../lib/js'));
}

exports.funcoes = funcoes;
exports.libJavascript = libJavascript;

//////////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////////////

function watcher() {
	watch(['sass/**/*.scss'], styles);
	// watch(['img/**/*.*'], images);
	watch(['js/funcoes/**/*.js'], funcoes);
}    
    
// watching
exports.watcher = watcher;


exports.build = series(fontes, fontStyles, styles, bibliotecasCSS, libJavascript, funcoes  );
exports.default = parallel(
    styles,
    funcoes,
    // bibliotecas, 
    watcher
);
