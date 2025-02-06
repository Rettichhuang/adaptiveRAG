PROMPTS = {}

PROMPTS[
    "generation_ess1"
] =     """Based on the provided aircraft parameters and checklist image, evaluate the conditions (e.g., IF, WHEN, AFFECTED) and determine the exact actions required to address the current situation.
        Focus exclusively on actionable steps by applying logical conditions to exclude irrelevant or redundant items. Present the results as clear, concise instructions.        Input format:
        - Current Warning: current_warning
        - Relevant Parameters: params
        - Checklist: checklist
        Output format:
        - Step 1: [Action]
        - Step 2: [Action]
        - Step 3: [Action]
        Requirements:
        1、Evaluate conditions from the checklist logically, based on the provided parameters.
        2、Exclude unnecessary steps, background context, or explanatory notes.
        3、Focus solely on immediate and critical actions for safety.

        Example 1:
        Input:
        - Current Warning: ENG 1 OIL LO PR
        - Relevant Parameters: Engine 1 oil pressure: 3 PSI; Engine 2 oil pressure: 59 PSI;Fuel Remaining: 7360 KG;Environmental Data: TAT +11°C, SAT 0°C; GW 62,400 KG
        - Checklist:
        ENG 1 OIL LO PR
        IF OIL PR < 13 PSI:
        1. Check oil pressure indication on the ECAM ENG page.
        2. **THR LEVER (of affected engine)**: IDLE
        3. **ENG MASTER (of affected engine)**: OFF 
        **Note**: 
        - If oil pressure is low (< 13 psi) is indicated only on ECAM ENG page (red indication) without the ENG OIL LO PR warning, it can be assumed that the oil pressure transducer is faulty. Flight crew may continue engine operation while monitoring other engine parameters.
        Output:
        - Step 1: THR LEVER 1...IDLE
        - Step 2: ENG MASTER 1...OFF
        
        Example 2:
        Input:
        - Current Warning: CAB PR SAFETY VALVE OPEN 
        - Relevant Parameters: Engine 1 oil pressure: 13 PSI; Engine 2 oil pressure: 36 PSI;Fuel Remaining: 7660 KG;Environmental Data: TAT +11°C, SAT 0°C; GW 62,400 KG;DIFF PR -3 PSI
        - Checklist:
        CAB PR SAFETY VALVE OPEN 
        The failure is probably due to an overpressure.
        IF DIFF PR ABV 8 PSI:
            MODE SEL...MAN
            MAN V/S CTL...AS RQRD
            L2 If overpressure is confirmed, reduce cabin ΔP.
            It may take 10 s in manual mode before the flight crew notices a change of the outflow valve position.
            IF UNSUCCESSFUL:
                A/C FL... REDUCE
        IF DIFF PR BELOW 0 PSI:
            EXPECT HI CAB RATE
            A/C V/S...REDUCE
            
           Output:
        - Step 1: A/C V/S...REDUCE
        ####      
        Real Data:
        Use the following input for your answer.
        Input:
        - Current Warning: {input_warning}
        - Relevant Parameters: {input_params}
        - Checklist: {input_checklist}
        Output: 
        """

PROMPTS = {}

PROMPTS[
    "generation_ess"
] = """Based on the provided aircraft parameters and checklist image, evaluate the conditions (e.g., IF, WHEN, AFFECTED) and determine the exact actions required to address the current situation.
        Focus exclusively on actionable steps by applying logical conditions to exclude irrelevant or redundant items. Present the results as clear, concise instructions.        Input format:
        - Current Warning: current_warning
        - Relevant Parameters: params
        - Checklist: checklist
        Output format:
        - Step 1: [Action]
        - Step 2: [Action]
        - Step 3: [Action]
        Requirements:
        1、Evaluate conditions from the checklist logically, based on the provided parameters.
        2、Exclude unnecessary steps, background context, or explanatory notes.
        3、Focus solely on immediate and critical actions for safety.

        Example 1:
        Input:
        - Current Warning: CAB PR SAFETY VALVE OPEN 
        - Relevant Parameters: Engine 1 oil pressure: 13 PSI; Engine 2 oil pressure: 36 PSI;Fuel Remaining: 7660 KG;Environmental Data: TAT +11°C, SAT 0°C; GW 62,400 KG;DIFF PR -3 PSI
        - Checklist:
        CAB PR SAFETY VALVE OPEN 
        The failure is probably due to an overpressure.
        IF DIFF PR ABV 8 PSI:
            MODE SEL...MAN
            MAN V/S CTL...AS RQRD
            L2 If overpressure is confirmed, reduce cabin ΔP.
            It may take 10 s in manual mode before the flight crew notices a change of the outflow valve position.
            IF UNSUCCESSFUL:
                A/C FL... REDUCE
        IF DIFF PR BELOW 0 PSI:
            EXPECT HI CAB RATE
            A/C V/S...REDUCE

           Output:
        - Step 1: A/C V/S...REDUCE
        ####      
        Real Data:
        Use the following input for your answer.
        Input:
        - Current Warning: {input_warning}
        - Relevant Parameters: {input_params}
        - Checklist: {input_checklist}
        Output: 
        """

