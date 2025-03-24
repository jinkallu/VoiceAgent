import React, { useState, useEffect } from "react";

const Solution = ({ token, index, step }) => {

    return (
        <div>

            <li key={index}>
                <strong>{step}</strong>
            </li>

        </div>
    );
};

export default Solution;
