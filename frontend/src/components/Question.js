import React, { Component } from "react";
import "../stylesheets/Question.css";

class Question extends Component {
	constructor() {
		super();
		this.state = {
			visibleAnswer: false,
		};
	}

	flipVisibility() {
		this.setState({ visibleAnswer: !this.state.visibleAnswer });
	}

	render() {
		const {
			questionId,
			question,
			answer,
			category,
			difficulty,
			rating,
		} = this.props;
		return (
			<div className="Question-holder">
				<div className="Question">{question}</div>
				<div className="Question-status">
					<img
						className="category"
						src={`${
							category.image_link ? category.image_link : category.type + ".svg"
						}`}
						alt="category"
					/>
					<div className="difficulty">Difficulty: {difficulty}</div>
					<div className="rating">Rating: {rating}</div>
					<img
						src="delete.png"
						className="delete action-img"
						onClick={() => this.props.questionAction("DELETE")}
						alt="category"
					/>
					<img
						src="edit.png"
						className="delete action-img"
						onClick={() => {
							this.props.history.push(`/questions/edit`, {
								questionId: questionId,
							});
						}}
						alt="category"
					/>
				</div>
				<div
					className="show-answer button"
					onClick={() => this.flipVisibility()}
				>
					{this.state.visibleAnswer ? "Hide" : "Show"} Answer
				</div>
				<div className="answer-holder">
					<span
						style={{
							visibility: this.state.visibleAnswer ? "visible" : "hidden",
						}}
					>
						Answer: {answer}
					</span>
				</div>
			</div>
		);
	}
}

export default Question;
