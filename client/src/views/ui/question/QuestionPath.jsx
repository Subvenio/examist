import React, { Children } from "react";
import { Link } from "react-router";
import { capitalize } from "lodash/string";
import QuestionIndex from "./QuestionIndex";
import { Box } from "../layout";

export default function QuestionPath(props) {
    const { full, question, paper, link } = props;
    let path = (
        <Box>
            { Children.toArray(question.formatted_path.map(segment => <QuestionIndex link={link} index={segment} />)) }
        </Box>
    );

    let paperDetail;
    if(full) {
        paperDetail = (
            <div className="paper-detail">
                <h3><Link to={link}>{ paper.year_start }</Link></h3>
                <h4><Link to={link}>{ capitalize(paper.period) }</Link></h4>
            </div>
        );
    }

    return (
        <div className="QuestionPath">
            { path }
            { paperDetail }
        </div>
    );
}