from flask import request
from flask_restx import abort, Namespace, Resource


from project.exceptions import ItemNotFound
from project.services import MovieService
from project.setup_db import db

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    def get(self):
        """Get all movies"""
        return (
            db.session.query(MovieService).get_all_movies()
        )


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, movie_id: int):
        """Get movie by id"""
        try:
            return MovieService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")
