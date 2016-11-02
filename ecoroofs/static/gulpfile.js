var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var sass = require('gulp-sass');

gulp.task('browser-sync', function() {
    browserSync.init({
        proxy: "http://localhost:8000/#!"
    });
});


gulp.task('sass', function() {
  return gulp.src('./*.scss')
    .pipe(sass())
    .pipe(gulp.dest('./'))
    .pipe(browserSync.reload({
      stream: true
    }))
});

gulp.task('watch', ['browser-sync', 'sass'], function (){
  gulp.watch('*.scss', {interval: 500}, ['sass']);
  gulp.watch('**/*.html', {interval: 500}, browserSync.reload);
  gulp.watch('**/*.js', {interval: 500}, browserSync.reload);
});
