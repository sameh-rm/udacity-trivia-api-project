import React, { Component } from "react";

import "../stylesheets/App.css";
import Question from "./Question";
import Search from "./Search";
import $ from "jquery";

class QuestionView extends Component {
	constructor() {
		super();
		this.state = {
			questions: [],
			page: 1,
			totalQuestions: 0,
			categories: {},
			currentCategory: null,
		};
	}

	componentDidMount() {
		this.getQuestions();
	}

	getQuestions = () => {
		$.ajax({
			url: `/questions?page=${this.state.page}`, //TODO: update request URL
			type: "GET",
			success: (result) => {
				this.setState({
					questions: result.questions,
					totalQuestions: result.total_questions,
					categories: result.categories,
					currentCategory: result.current_category,
				});
				return;
			},
			error: (error) => {
				alert("Unable to load questions. Please try your request again");
				return;
			},
		});
	};

	selectPage(num) {
		this.setState({ page: num }, () => this.getQuestions());
	}

	createPagination() {
		let pageNumbers = [];
		let maxPage = Math.ceil(this.state.totalQuestions / 10);
		for (let i = 1; i <= maxPage; i++) {
			pageNumbers.push(
				<span
					key={i}
					className={`page-num ${i === this.state.page ? "active" : ""}`}
					onClick={() => {
						this.selectPage(i);
					}}
				>
					{i}
				</span>
			);
		}
		return pageNumbers;
	}

	getByCategory = (id) => {
		$.ajax({
			url: `/categories/${id}/questions`, //TODO: update request URL
			type: "GET",
			success: (result) => {
				this.setState({
					questions: result.questions,
					totalQuestions: result.total_questions,
					currentCategory: result.current_category,
				});
				return;
			},
			error: (error) => {
				alert("Unable to load questions. Please try your request again");
				return;
			},
		});
	};

	submitSearch = (searchTerm) => {
		$.ajax({
			url: `/questions/search`, //TODO: update request URL
			type: "POST",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({ searchTerm: searchTerm }),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {
				this.setState({
					questions: result.questions,
					totalQuestions: result.total_questions,
					currentCategory: result.current_category,
				});
				return;
			},
			error: (error) => {
				alert("Unable to load questions. Please try your request again");
				return;
			},
		});
	};
	deleteCategory = (id) => {
		if (window.confirm("are you sure you want to delete the category?")) {
			$.ajax({
				url: `/categories/${id}`, //TODO: update request URL
				type: "DELETE",
				headers: {
					"xx-auth-token": this.props.token,
				},
				success: (result) => {
					this.getQuestions();
				},
				error: (error) => {
					alert("Unable to delete this category. Please login and try again");
					return;
				},
			});
		}
	};
	questionAction = (id) => (action) => {
		switch (action) {
			case "DELETE":
				if (window.confirm("are you sure you want to delete the question?")) {
					$.ajax({
						url: `/questions/${id}`, //TODO: update request URL
						type: "DELETE",
						dataType: "json",
						contentType: "applicaiton/json",
						headers: {
							"xx-auth-token": this.props.token,
						},
						success: (result) => {
							this.getQuestions();
						},
						error: (error) => {
							alert("Unable to load questions. Please try your request again");
							return;
						},
					});
				}
				break;

			default:
				return;
		}
	};

	render() {
		return (
			<div className="question-view">
				<div className="categories-list">
					<h2
						onClick={() => {
							this.getQuestions();
						}}
					>
						Categories
					</h2>
					{this.state.categories.length > 0 ? (
						<ul>
							{this.state.categories.map((category) => {
								return (
									<li className="category-item" key={category.id * 50}>
										<div
											className="category-left"
											onClick={() => {
												this.getByCategory(category.id);
											}}
										>
											<img
												className="category"
												src={
													!category.image_link
														? `${category.type}.svg`
														: category.image_link
												}
												alt={category.type}
											/>
											<p className="category-type">{category.type}</p>
										</div>
										<img
											src="delete.png"
											className="delete action-img"
											onClick={() => this.deleteCategory(category.id)}
											alt="category"
										/>
										<img
											src="edit.png"
											className="delete action-img"
											onClick={() => {
												this.props.history.push(`/categories/edit`, {
													categoryId: category.id,
												});
											}}
											alt="category"
										/>
									</li>
								);
							})}
						</ul>
					) : (
						<h3>No Categories</h3>
					)}
					<Search submitSearch={this.submitSearch} />
				</div>
				<div className="questions-list">
					<h2>Questions</h2>
					{this.state.questions.length > 0 ? (
						this.state.questions.map((q, ind) => {
							return (
								<Question
									key={q.id}
									question={q.question}
									answer={q.answer}
									category={q.category}
									difficulty={q.difficulty}
									rating={q.rating}
									questionAction={this.questionAction(q.id)}
									questionId={q.id}
									history={this.props.history}
								/>
							);
						})
					) : (
						<h2>There is no questions</h2>
					)}
					<div className="pagination-menu">{this.createPagination()}</div>
				</div>
			</div>
		);
	}
}

export default QuestionView;
