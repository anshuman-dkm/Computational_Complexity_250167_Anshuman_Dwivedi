"""


This module implements:
1. Single-Tape Turing Machine - Basic Turing M with one tape and one read/write head
2. Two-Tape Turing Machine - Extended Turing M with two tapes and two heads

Examples included in this module:
- Binary Increment (Single-Tape): Adds 1 to a binary number
- Palindrome Detection (Two-Tape): Checks if a string is a palindrome
- Efficiency Comparison: Demonstrates O(n²) vs O(n) for a special string copying

Anshuman Dwivedi_250167
"""




class SingleTapeTuringMachine:
    """
    
    The machine has:
    - One infinite tape (represented as a list)
    - One read/write head that moves left or right
    - A finite set of states with one initial and one or more halt states
    - A transition function: (state, symbol) -> (new_state, write_symbol, direction)
    """
    
    def __init__(self, tape_input, blank_symbol='_', initial_state='q0', halt_states=None):
        """
        Initialize the Single-Tape Turing Machine.
        
        Parameters:
        
        tape_input : str or list
            The initial content to place on the tape
        blank_symbol : str
            Symbol representing blank/empty cells (default: '_')
        initial_state : str
            The starting state of the machine (default: 'q0')
        halt_states : set
            Set of accepting/halting states (default: {'qhalt'})
        """
        # Convert input string to list for the tape
        self.tape = list(tape_input) if tape_input else [blank_symbol]
        
        # Blank symbol for empty cells
        self.blank_symbol = blank_symbol
        
        # Current state of the machine
        self.current_state = initial_state
        
        # Head position (starts at leftmost position)
        self.head_position = 0
        
        # Halting states - machine stops when reaching these
        self.halt_states = halt_states if halt_states else {'qhalt'}
        
        # Transition function stored as dictionary
        # Key: (current_state, read_symbol)
        # Value: (new_state, write_symbol, direction)
        self.transitions = {}
        
        # Step counter for efficiency measurement
        self.step_count = 0
    
    def add_transition(self, current_state, read_symbol, new_state, write_symbol, direction):
        """
        Add a single transition rule to the machine.
        
        Parameters:
      
        current_state : str
            The state before transition
        read_symbol : str
            The symbol read from tape
        new_state : str
            The state after transition
        write_symbol : str
            The symbol to write on tape
        direction : str
            'L' for left, 'R' for right, 'S' for stay
        """
        self.transitions[(current_state, read_symbol)] = (new_state, write_symbol, direction)
    
    def display_tape(self, show_state=True):
        """
        Display the current tape configuration with head position.
        
        The head position is shown with brackets around the current symbol.
        """
        # Build tape display string
        tape_display = ""
        for i, symbol in enumerate(self.tape):
            if i == self.head_position:
                # Highlight current head position with brackets
                tape_display += f"[{symbol}]"
            else:
                tape_display += f" {symbol} "
        
        if show_state:
            print(f"State: {self.current_state} | Tape: {tape_display}")
        else:
            print(f"Tape: {tape_display}")
    
    def step(self):
        """
        Execute a single step (transition) of the Turing Machine.
        
        Returns:
        bool : True if step was executed, False if machine halted
        """
        # Check if already in halt state
        if self.current_state in self.halt_states:
            return False
        
        # Extend tape if head goes beyond current bounds
        while self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
        while self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        
        # Read symbol at current head position
        read_symbol = self.tape[self.head_position]
        
        # Look up transition
        key = (self.current_state, read_symbol)
        if key not in self.transitions:
            print(f"No transition defined for state '{self.current_state}' and symbol '{read_symbol}'")
            return False
        
        # Get transition details
        new_state, write_symbol, direction = self.transitions[key]
        
        # Write symbol to tape
        self.tape[self.head_position] = write_symbol
        
        # Move head
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'S' means stay in place
        
        # Update state
        self.current_state = new_state
        
        # Increment step counter
        self.step_count += 1
        
        return True
    
    def run(self, max_steps=1000, verbose=False):
        """
        
        
        Parameters:
        
        max_steps : int
            Maximum steps to prevent infinite loops
        verbose : bool
            If True, display tape after each step
        
        Returns:
        --------
        bool : True if machine halted normally, False if max steps reached
        """
        if verbose:
            print("Initial configuration:")
            self.display_tape()
           
        
        while self.step_count < max_steps:
            if not self.step():
                if verbose:
                    
                    print("Machine halted!")
                    self.display_tape()
                return True
            
            if verbose:
                self.display_tape()
        
        print("Warning: Maximum steps reached!")
        return False
    
    def get_tape_content(self):
        """Return the tape content as a string, stripping blank symbols from ends."""
        result = ''.join(self.tape)
        return result.strip(self.blank_symbol)




class TwoTapeTuringMachine:
    """
   
    
    The machine has:
    - Two infinite tapes (each represented as a list)
    - Two independent read/write heads
    - A finite set of states
    - A transition function: (state, symbol1, symbol2) -> 
                             (new_state, write1, dir1, write2, dir2)
    
    This demonstrates how an additional tape can improve efficiency
    for certain problems (e.g., palindrome checking).
    """
    
    def __init__(self, tape1_input, tape2_input='', blank_symbol='_', 
                 initial_state='q0', halt_states=None):
        """
        Initialize the Two-Tape Turing Machine.
        
        Parameters:
        -----------
        tape1_input : str or list
            Initial content for tape 1 (usually the input)
        tape2_input : str or list
            Initial content for tape 2 (usually empty for scratch space)
        blank_symbol : str
            Symbol representing blank/empty cells
        initial_state : str
            The starting state of the machine
        halt_states : set
            Set of accepting/halting states
        """
        # Initialize both tapes
        self.tape1 = list(tape1_input) if tape1_input else [blank_symbol]
        self.tape2 = list(tape2_input) if tape2_input else [blank_symbol]
        
        # Blank symbol
        self.blank_symbol = blank_symbol
        
        # Current state
        self.current_state = initial_state
        
        # Two head positions (one for each tape)
        self.head1_position = 0
        self.head2_position = 0
        
        # Halting states
        self.halt_states = halt_states if halt_states else {'qhalt'}
        
        # Transition function
        # Key: (current_state, symbol_tape1, symbol_tape2)
        # Value: (new_state, write1, dir1, write2, dir2)
        self.transitions = {}
        
        # Step counter
        self.step_count = 0
    
    def add_transition(self, current_state, read1, read2, new_state, 
                       write1, dir1, write2, dir2):
        """
        Parameters:
        -----------
        current_state : str
            Current state before transition
        read1 : str
            Symbol read from tape 1
        read2 : str
            Symbol read from tape 2
        new_state : str
            State after transition
        write1 : str
            Symbol to write on tape 1
        dir1 : str
            Direction for head 1 ('L', 'R', or 'S')
        write2 : str
            Symbol to write on tape 2
        dir2 : str
            Direction for head 2 ('L', 'R', or 'S')
        """
        key = (current_state, read1, read2)
        value = (new_state, write1, dir1, write2, dir2)
        self.transitions[key] = value
    
    def display_tapes(self, show_state=True):
        """
        Display both tapes with their head positions.
        """
        # Display tape 1
        tape1_display = ""
        for i, symbol in enumerate(self.tape1):
            if i == self.head1_position:
                tape1_display += f"[{symbol}]"
            else:
                tape1_display += f" {symbol} "
        
        # Display tape 2
        tape2_display = ""
        for i, symbol in enumerate(self.tape2):
            if i == self.head2_position:
                tape2_display += f"[{symbol}]"
            else:
                tape2_display += f" {symbol} "
        
        if show_state:
            print(f"State: {self.current_state}")
        print(f"  Tape 1: {tape1_display}")
        print(f"  Tape 2: {tape2_display}")
    
    def _extend_tape_if_needed(self, tape, head_pos):
        """Extend tape if head goes beyond current bounds."""
        while head_pos >= len(tape):
            tape.append(self.blank_symbol)
        return tape, max(0, head_pos)
    
    def step(self):
        """
        Execute a single step of the Two-Tape Turing Machine.
        
        Returns:
        --------
        bool : True if step was executed, False if halted
        """
        # Check if in halt state
        if self.current_state in self.halt_states:
            return False
        
        # Extend tapes if needed
        self.tape1, self.head1_position = self._extend_tape_if_needed(
            self.tape1, self.head1_position)
        self.tape2, self.head2_position = self._extend_tape_if_needed(
            self.tape2, self.head2_position)
        
        # Read symbols from both tapes
        read1 = self.tape1[self.head1_position]
        read2 = self.tape2[self.head2_position]
        
        # Look up transition
        key = (self.current_state, read1, read2)
        if key not in self.transitions:
            print(f"No transition for state='{self.current_state}', "
                  f"tape1='{read1}', tape2='{read2}'")
            return False
        
        # Get transition
        new_state, write1, dir1, write2, dir2 = self.transitions[key]
        
        # Write to both tapes
        self.tape1[self.head1_position] = write1
        self.tape2[self.head2_position] = write2
        
        # Move heads
        if dir1 == 'R':
            self.head1_position += 1
        elif dir1 == 'L':
            self.head1_position -= 1
        
        if dir2 == 'R':
            self.head2_position += 1
        elif dir2 == 'L':
            self.head2_position -= 1
        
        # Handle negative positions by inserting at beginning
        if self.head1_position < 0:
            self.tape1.insert(0, self.blank_symbol)
            self.head1_position = 0
        if self.head2_position < 0:
            self.tape2.insert(0, self.blank_symbol)
            self.head2_position = 0
        
        # Update state
        self.current_state = new_state
        self.step_count += 1
        
        return True
    
    def run(self, max_steps=1000, verbose=False):
        """
        Run the machine until it halts or reaches max steps.
        
        Parameters:
        -----------
        max_steps : int
            Maximum steps to prevent infinite loops
        verbose : bool
            If True, display tapes after each step
        
        Returns:
        --------
        bool : True if halted normally, False if max steps reached
        """
        if verbose:
            print("Initial configuration:")
            self.display_tapes()
          
        
        while self.step_count < max_steps:
            if not self.step():
                if verbose:
                    print("Machine halted!")
                    self.display_tapes()
                return True
            
            if verbose:
                self.display_tapes()
                print()
        
        print("Warning: Maximum steps reached!")
        return False



def binary_increment_example():
    """
    Demonstrate Single-Tape TM: Increment a binary number by 1.
    
    Algorithm:
    1. Move to the rightmost bit
    2. If it's '0', change to '1' and halt
    3. If it's '1', change to '0' and move left (carry)
    4. If at blank (leftmost), add '1' and halt
    
    Example: 1011 -> 1100
             (11 in decimal -> 12 in decimal)
    """

    print("EXAMPLE 1: Binary Increment using Single-Tape Turing Machine")

    print()
    
    # Input binary number
    binary_input = "1011"
    print(f"Input binary number: {binary_input}")
    print(f"Decimal equivalent: {int(binary_input, 2)}")
    print()
    
    # Create the Turing Machine
    tm = SingleTapeTuringMachine(
        tape_input=binary_input,
        blank_symbol='_',
        initial_state='q0',
        halt_states={'qhalt'}
    )
    
    # Define transitions
    # State q0: Move right to find end of number
    tm.add_transition('q0', '0', 'q0', '0', 'R')  # Read 0, stay in q0, move right
    tm.add_transition('q0', '1', 'q0', '1', 'R')  # Read 1, stay in q0, move right
    tm.add_transition('q0', '_', 'q1', '_', 'L')  # Found blank, go back left, change to q1
    
    # State q1: Process the increment (from right to left)
    tm.add_transition('q1', '0', 'qhalt', '1', 'S')  # 0 -> 1, no carry, halt
    tm.add_transition('q1', '1', 'q1', '0', 'L')     # 1 -> 0, carry, move left
    tm.add_transition('q1', '_', 'qhalt', '1', 'S')  # Blank -> 1, halt (overflow case)
    
    print("Running the Turing Machine step by step:")
    print("-" * 50)
    
    # Run with verbose output
    tm.run(verbose=True)
    
    # Get result
    result = tm.get_tape_content()
    print()
    print(f"Result binary number: {result}")
    print(f"Decimal equivalent: {int(result, 2)}")
    print(f"Total steps taken: {tm.step_count}")
    print()
    
    return tm.step_count



def palindrome_example():
    """
    Demonstrate Two-Tape TM: Check if a string is a palindrome.
    
    Algorithm using Two Tapes:
    1. Copy input from Tape 1 to Tape 2 while moving right
    2. Reset head on Tape 1 to the beginning
    3. Compare Tape 1 (left to right) with Tape 2 (right to left)
    4. If all symbols match, it's a palindrome
    
    This is more efficient than single-tape because we don't need
    to repeatedly traverse the entire string.
    """

    print("EXAMPLE 2: Palindrome Detection using Two-Tape Turing Machine")

    print()
    
    # Test with a palindrome
    test_input = "abba"
    print(f"Testing string: '{test_input}'")
    print()
    
    # Create Two-Tape TM
    tm = TwoTapeTuringMachine(
        tape1_input=test_input,
        tape2_input='',
        blank_symbol='_',
        initial_state='copy',
        halt_states={'accept', 'reject'}
    )
    
    # Phase 1: Copy from Tape 1 to Tape 2
    # State 'copy': Copy each symbol from Tape 1 to Tape 2
    for symbol in ['a', 'b', 'c', 'd']:  # Add more symbols as needed
        tm.add_transition('copy', symbol, '_', 'copy', symbol, 'R', symbol, 'R')
    tm.add_transition('copy', '_', '_', 'reset', '_', 'L', '_', 'S')
    
    # Phase 2: Reset - Move Tape 1 head back to beginning, Tape 2 stays at end
    for symbol in ['a', 'b', 'c', 'd']:
        tm.add_transition('reset', symbol, '_', 'reset', symbol, 'L', '_', 'S')
    tm.add_transition('reset', '_', '_', 'compare', '_', 'R', '_', 'L')
    
    # Phase 3: Compare - Match Tape 1 (forward) with Tape 2 (backward)
    for symbol in ['a', 'b', 'c', 'd']:
        # Matching symbols - continue comparing
        tm.add_transition('compare', symbol, symbol, 'compare', symbol, 'R', symbol, 'L')
        # Non-matching symbols - reject
        for other in ['a', 'b', 'c', 'd']:
            if other != symbol:
                tm.add_transition('compare', symbol, other, 'reject', symbol, 'S', other, 'S')
    
    # Reached end of both strings successfully - accept
    tm.add_transition('compare', '_', '_', 'accept', '_', 'S', '_', 'S')
    
    print("Running the Two-Tape Turing Machine:")
    
    
    # Run with verbose output
    tm.run(verbose=True)
    
    print()
    if tm.current_state == 'accept':
        print(f"Result: '{test_input}' IS a palindrome!")
    else:
        print(f"Result: '{test_input}' is NOT a palindrome.")
    print(f"Total steps taken: {tm.step_count}")
    print()
    
    # Also test a non-palindrome
    
    print("Testing a non-palindrome...")
    print()
    
    test_input2 = "abc"
    print(f"Testing string: '{test_input2}'")
    
    tm2 = TwoTapeTuringMachine(
        tape1_input=test_input2,
        tape2_input='',
        blank_symbol='_',
        initial_state='copy',
        halt_states={'accept', 'reject'}
    )
    
    # Add same transitions
    for symbol in ['a', 'b', 'c', 'd']:
        tm2.add_transition('copy', symbol, '_', 'copy', symbol, 'R', symbol, 'R')
    tm2.add_transition('copy', '_', '_', 'reset', '_', 'L', '_', 'S')
    
    for symbol in ['a', 'b', 'c', 'd']:
        tm2.add_transition('reset', symbol, '_', 'reset', symbol, 'L', '_', 'S')
    tm2.add_transition('reset', '_', '_', 'compare', '_', 'R', '_', 'L')
    
    for symbol in ['a', 'b', 'c', 'd']:
        tm2.add_transition('compare', symbol, symbol, 'compare', symbol, 'R', symbol, 'L')
        for other in ['a', 'b', 'c', 'd']:
            if other != symbol:
                tm2.add_transition('compare', symbol, other, 'reject', symbol, 'S', other, 'S')
    
    tm2.add_transition('compare', '_', '_', 'accept', '_', 'S', '_', 'S')
    
    tm2.run(verbose=False)
    
    if tm2.current_state == 'accept':
        print(f"Result: '{test_input2}' IS a palindrome!")
    else:
        print(f"Result: '{test_input2}' is NOT a palindrome.")
    print(f"Total steps taken: {tm2.step_count}")
    print()
    
    return tm.step_count


def compare_efficiency():
    """
    
    Problem: Copy a string (simulate marking/counting elements)
    
    Single-Tape Complexity: O(n²) - must traverse back and forth
    Two-Tape Complexity: O(n) - linear pass using second tape
    
    This demonstrates the fundamental efficiency advantage of 
    additional computational resources (extra tape).
    """
    print("EFFICIENCY COMPARISON: Single-Tape vs Two-Tape TM") 
    print()
    print("Problem: Copy/process a string of length n")
    print("Single-Tape: O(n²) - must traverse back and forth for each symbol")
    print("Two-Tape: O(n) - copy directly using the second tape")
    print()
    
    # Test with different input sizes
    test_sizes = [4, 8, 12]
    
   
    print(f"{'Input Size':<12} {'Single-Tape Steps':<20} {'Two-Tape Steps':<20}")
    
    
    results = []
    
    for size in test_sizes:
        # Generate test input (alternating a's and b's)
        test_input = ''.join(['a' if i % 2 == 0 else 'b' for i in range(size)])
        
        # ----- SINGLE-TAPE: String Mark-and-Copy -----
        # This simulates marking each character and moving it to the end
        # Requires O(n) passes, each traversing O(n) -> O(n²) total
        
        single_tm = SingleTapeTuringMachine(
            tape_input=test_input + '_' * size,  # Input + space for copy
            blank_symbol='_',
            initial_state='find',
            halt_states={'done'}
        )
        
        # Transitions for marking and copying each character
        # State 'find': Find next unmarked character
        single_tm.add_transition('find', 'a', 'carry_a', 'X', 'R')
        single_tm.add_transition('find', 'b', 'carry_b', 'X', 'R')
        single_tm.add_transition('find', 'X', 'find', 'X', 'R')
        single_tm.add_transition('find', '_', 'done', '_', 'S')  # All done
        
        # State 'carry_a': Carry 'a' to the copy section
        single_tm.add_transition('carry_a', 'a', 'carry_a', 'a', 'R')
        single_tm.add_transition('carry_a', 'b', 'carry_a', 'b', 'R')
        single_tm.add_transition('carry_a', 'X', 'carry_a', 'X', 'R')
        single_tm.add_transition('carry_a', '_', 'return', 'a', 'L')  # Place 'a'
        single_tm.add_transition('carry_a', 'A', 'carry_a', 'A', 'R')
        single_tm.add_transition('carry_a', 'B', 'carry_a', 'B', 'R')
        
        # State 'carry_b': Carry 'b' to the copy section
        single_tm.add_transition('carry_b', 'a', 'carry_b', 'a', 'R')
        single_tm.add_transition('carry_b', 'b', 'carry_b', 'b', 'R')
        single_tm.add_transition('carry_b', 'X', 'carry_b', 'X', 'R')
        single_tm.add_transition('carry_b', '_', 'return', 'b', 'L')  # Place 'b'
        single_tm.add_transition('carry_b', 'A', 'carry_b', 'A', 'R')
        single_tm.add_transition('carry_b', 'B', 'carry_b', 'B', 'R')
        
        # State 'return': Go back to find next unmarked character
        single_tm.add_transition('return', 'a', 'return', 'a', 'L')
        single_tm.add_transition('return', 'b', 'return', 'b', 'L')
        single_tm.add_transition('return', 'A', 'return', 'A', 'L')
        single_tm.add_transition('return', 'B', 'return', 'B', 'L')
        single_tm.add_transition('return', 'X', 'find', 'X', 'R')  # Found marked, look for next
        
        single_tm.run(max_steps=5000, verbose=False)
        single_steps = single_tm.step_count
        
        # ----- TWO-TAPE: Direct Copy -----
        # Simple O(n) copy - read from tape 1, write to tape 2
        
        two_tm = TwoTapeTuringMachine(
            tape1_input=test_input,
            tape2_input='',
            blank_symbol='_',
            initial_state='copy',
            halt_states={'done'}
        )
        
        # Copy each symbol from Tape 1 to Tape 2 in one pass
        two_tm.add_transition('copy', 'a', '_', 'copy', 'a', 'R', 'a', 'R')
        two_tm.add_transition('copy', 'b', '_', 'copy', 'b', 'R', 'b', 'R')
        two_tm.add_transition('copy', '_', '_', 'done', '_', 'S', '_', 'S')
        
        two_tm.run(max_steps=5000, verbose=False)
        two_steps = two_tm.step_count
        
        print(f"{size:<12} {single_steps:<20} {two_steps:<20}")
        results.append((size, single_steps, two_steps))
    
    print("-" * 60)
    print()
    print("ANALYSIS:")
    print("-" * 60)
    print()
    
    # Show the efficiency difference
    for size, single, two in results:
        ratio = single / two if two > 0 else 0
        print(f"Input size {size}:")
        print(f"  Single-Tape: {single} steps")
        print(f"  Two-Tape: {two} steps")
        print(f"  Speedup: {ratio:.1f}x faster with Two-Tape")
        print()
    
    print("CONCLUSION:")
   
    print("The Two-Tape Turing Machine is significantly more efficient")
    print("for the string copying problem:")
    print("  - Single-Tape: O(n²) time complexity")
    print("  - Two-Tape: O(n) time complexity")
    print()
    print("This demonstrates that adding computational resources (extra tape)")
    print("can fundamentally improve the efficiency of algorithms.")
    print()




def main():
   
    print()
    print("|" + " MULTI-TAPE TURING MACHINE ".center(58) + "|")
    print()
    
    while True:
        print("\nSelect an option:")
        print("1. Binary Increment (Single-Tape TM)")
        print("2. Palindrome Detection (Two-Tape TM)")
        print("3. Efficiency Comparison")
        print("4. Run All Examples")
        print("5. Exit")
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
        except EOFError:
            # Handle non-interactive mode
            print("\nRunning all examples automatically...")
            choice = '4'
        
        print()
        
        if choice == '1':
            binary_increment_example()
        elif choice == '2':
            palindrome_example()
        elif choice == '3':
            compare_efficiency()
        elif choice == '4':
            print("Running all examples...")
            print()
            binary_increment_example()
            palindrome_example()
            compare_efficiency()
            print("\nAll examples completed!")
            break
        elif choice == '5':
            print("Thank you")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
