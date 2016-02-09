import React, { Component } from "react";
import { connect } from "react-redux";
import { isPending } from "redux-pending";
import * as model from "../../model";
import { Loading, Empty } from "../ui";
import { QuestionList } from "../ui/question";
import { PaperFooter } from "../ui/paper";

class Paper extends Component {
    static selector = (state, props) => ({
        paper: model.resources.Paper.selectPaperWithQuestions(props.params)(state),
        isLoadingPaper: isPending(model.resources.Paper.getPaper)(state)
    });

    static actions = {
        getPaper: model.resources.Paper.getPaper
    };

    componentWillMount() {
        const { paper, params: { module, year, period } } = this.props;

        // When we directly link to the paper
        if(!paper)
            this.props.getPaper(module, year, period);
    }

    componentWillReceiveProps(props) {
        const { isLoadingPaper, params: { module, year, period } } = props;

        // Previous state
        let prevModule = this.props.params.module;
        let prevYear = this.props.params.year;
        let prevPeriod = this.props.params.period;

        if(!isLoadingPaper && (prevModule !== module || prevYear !== year || prevPeriod !== period))
            this.props.getPaper(module, year, period);
    }

    render() {
        const { isLoadingPaper, paper } = this.props;

        if(isLoadingPaper) {
            return <Loading />
        }

        if(!paper) {
            return <Empty/>
        }

        const questions = paper.questions;
        let content = <Empty/>;

        if(questions && questions.length) {
            content = <QuestionList questions={questions} />
        }

        return (
            <div className="Paper">
                <h3>Questions</h3>
                { content }
                <PaperFooter paper={paper} />
            </div>
        );
    }
}

export default connect(Paper.selector, Paper.actions)(Paper);