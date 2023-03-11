const { src, dest, watch, parallel, series } = require('gulp');

const scss = require('gulp-sass')(require('sass'));
const concat = require('gulp-concat');
const autoprefixer = require('gulp-autoprefixer');
const uglify = require('gulp-uglify');
const imagemin = require('gulp-imagemin'); // WARNING!! > PRECISA INTALAR ESSA: npm install --save-dev gulp-imagemin@7.1.0
const browserSync = require('browser-sync').create();
// const del = require('del');

// function browsersync() {
// 	browserSync.init({
// 		server: {
// 			baseDir: 'app/',
// 		},
// 		notify: false,
// 	});
// }
function libCssExternal() {
	return src(['terceiros/bootstrap/scss/bootstrap.scss', 'terceiros/caroucel/owl.carousel/src/scss/owl.carousel.scss'], {sourcemaps: true})
		.pipe(scss({ outputStyle: 'compressed' }))
		// .pipe(concat('bootstrap.min.css'))
		.pipe(
			autoprefixer({
				overrideBrowserslist: ['last 15 versions'],
				grid: true,
			})
		)
		.pipe(dest('../lib/css/'));
		// .pipe(browserSync.stream());
}

function styles() {
	return src('sass/estilos.scss', {sourcemaps: true})
		.pipe(scss({ outputStyle: 'compressed' }))
		.pipe(concat('estilos.min.css'))
		.pipe(
			autoprefixer({
				overrideBrowserslist: ['last 15 versions'],
				grid: true,
			})
		)
		.pipe(dest('../lib/css/'));
		// .pipe(browserSync.stream());
}
// function fontsBrand() {
// 	return src('fontes/stylesheet.css', {sourcemaps: true})
// 		.pipe(scss({ outputStyle: 'compressed' }))
// 		.pipe(concat('fontBrand.min.css'))
// 		.pipe(
// 			autoprefixer({
// 				overrideBrowserslist: ['last 15 versions'],
// 				grid: true,
// 			})
// 		)
// 		.pipe(dest('../lib/css/'));
// }
// function fontsBrandLib() {
// 	return src([
//             'fontes/*.eot',
//             'fontes/*.ttf',
//             'fontes/*.woff'
//         ])
//     .pipe(dest('../lib/fontes/'));
// }

function scriptsCustom() {
	return src( 'js/prod/**/*.js', {sourcemaps: true})
		.pipe(concat('main.min.js'))
		.pipe(uglify())
		.pipe(dest('../lib/js'));
		// .pipe(browserSync.stream());
}
function scripts() {
	return src( 'js/lib/**/*.js', {sourcemaps: true})
		// .pipe(concat('scripts.min.js'))
		.pipe(uglify())
		.pipe(dest('../lib/js'));
		// .pipe(browserSync.stream());
}


function images() {
	return src('img/**/*.*')
		.pipe(
			imagemin([
				imagemin.gifsicle({ interlaced: true }),
				imagemin.mozjpeg({ quality: 75, progressive: true }),
				imagemin.optipng({ optimizationLevel: 5 }),
				imagemin.svgo({
					plugins: [{ removeViewBox: true }, { cleanupIDs: false }],
				}),
			])
		)
		.pipe(dest('../lib/img'));
		// .pipe(browserSync.stream());
}

function build() {
	return src(['app/**/*.html', 'app/css/style.min.css', 'app/js/main.min.js'], { base: 'app' })
	.pipe(dest('../lib/'));
}

// function cleanDist() {
// 	 return del('dist/');
// }

function watching() {
	watch(['sass/**/*.scss'], styles);
	// watch(['images/**/*.*'], images);
	// watch(['js/prod/**/*.js'], scriptsCustom);
}

function watchRecursos() {
	// watch(['sass/**/*.scss'], styles);
	watch(['img/**/*.*'], images);
	watch(['js/prod/**/*.js'], scriptsCustom);
}
exports.libCssExternal = libCssExternal;
// exports.fontsBrand = fontsBrand;
// exports.fontsBrandLib = fontsBrandLib;
exports.styles = styles;
exports.scripts = scripts;
exports.scriptsCustom = scriptsCustom;
exports.images = images;
// exports.browsersync = browsersync;
// exports.cleanDist = cleanDist;
exports.watching = watching;
exports.watchRecursos = watchRecursos;
exports.build = series(images, build);

exports.default = parallel(
	libCssExternal,
	// fontsBrand,
	// fontsBrandLib,
	styles,
	scripts,
	scriptsCustom,
	images,
	// browsersync,
	// watching
	);
