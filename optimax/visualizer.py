import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from optimax.parser import ProblemInstance
from networkx.drawing.nx_agraph import graphviz_layout

class Visualizer:
    @staticmethod
    def plot_feasible_region(problem: ProblemInstance, solution: dict, filename="feasible_region.png"):
        """
        Visualizes the feasible region for 2-variable LP problems.
        Plots constraint lines, shades the feasible region, and marks the optimal solution.
        
        Parameters:
            problem (ProblemInstance): The optimization problem instance.
            solution (dict): The solution dictionary with at least 'variables' key.
            filename (str): The file name where the plot will be saved.
        """
        num_vars = len(problem.function_objective)
        if num_vars != 2:
            print("Feasible region visualization is only supported for 2-variable problems.")
            return

        # Define a grid for plotting
        x = np.linspace(0, 50, 400)
        y = np.linspace(0, 50, 400)
        X, Y = np.meshgrid(x, y)
        
        fig, ax = plt.subplots()
        
        # Initialize a mask for the feasible region (start with all True)
        feasible_mask = np.ones_like(X, dtype=bool)
        
        # Plot each constraint and update the feasible mask
        for cons in problem.constraints:
            coef = cons["coeficientes"]
            sign = cons["signo"]
            rhs = cons["valor"]
            
            # Plot constraint lines (avoid division by zero)
            if coef[1] != 0:
                # Calculate line: y = (rhs - coef[0]*x)/coef[1]
                y_line = (rhs - coef[0] * x) / coef[1]
                ax.plot(x, y_line, label=f'{coef[0]}x + {coef[1]}y {sign} {rhs}')
            else:
                # Vertical line: x = rhs/coef[0]
                x_line = np.full_like(y, rhs / coef[0])
                ax.plot(x_line, y, label=f'{coef[0]}x {sign} {rhs}')
            
            # Update the feasible mask based on the constraint
            if sign == '<=':
                feasible_mask &= (coef[0] * X + coef[1] * Y <= rhs)
            elif sign == '>=':
                feasible_mask &= (coef[0] * X + coef[1] * Y >= rhs)
            elif sign == '==':
                feasible_mask &= np.isclose(coef[0] * X + coef[1] * Y, rhs, atol=1e-2)
            else:
                raise ValueError(f"Unsupported constraint sign: {sign}")
        
        # Shade the feasible region
        ax.contourf(X, Y, feasible_mask, levels=[0.5, 1], colors=['#cce5ff'], alpha=0.5)
        
        # Plot the optimal solution if available
        if "variables" in solution:
            opt_x, opt_y = solution["variables"]
            ax.plot(opt_x, opt_y, 'ro', label='Optimal Solution')
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.set_title('Feasible Region')
        
        # Save the figure as a PNG file
        plt.savefig(filename)
        plt.close(fig)  # Close the plot after saving

    @staticmethod
    def plot_convergence(iterations, objective_values, filename="convergence_graph.png"):
        """
        Plots the convergence graph of the optimization process.
        
        Parameters:
            iterations (list): List of iteration numbers.
            objective_values (list): Corresponding objective function values.
            filename (str): The file name where the plot will be saved.
        """
        plt.figure()
        plt.plot(iterations, objective_values, marker='o')
        plt.xlabel('Iteration')
        plt.ylabel('Objective Value')
        plt.title('Convergence Graph')
        plt.grid(True)
        
        # Save the figure as a PNG file
        plt.savefig(filename)
        plt.close()  # Close the plot after saving
    
    @staticmethod
    def plot_branch_and_bound_tree(branch_tree_data, filename="branch_and_bound_tree.png"):
        """
        Visualizes the Branch & Bound tree using NetworkX.

        Parameters:
            branch_tree_data (list): List of dictionaries representing nodes in the tree.
                Each dictionary should contain:
                    - 'node_id': Unique identifier for the node.
                    - 'parent_id': Parent node ID (if any).
                    - 'bounds': The current bounds (optional).
                    - 'variables': The variables and their current values (optional).
                    - 'depth': Depth of the node in the tree.
                    - 'objective_value': The objective value of the node (optional).
                    - 'branch_decision': The decision made to branch (optional).
            filename (str): The file name where the plot will be saved.
        """
        G = nx.DiGraph()  # Directed graph

        # Add nodes and edges to the graph based on the branch tree data
        for node in branch_tree_data:
            node_id = node['node_id']
            parent_id = node.get('parent_id', None)
            objective_value = node.get('objective_value', 'N/A')
            branch_decision = node.get('branch_decision', '')

            # Node label including ID, decision, and objective value
            node_label = f"{node_id}\n{branch_decision}\nZ={objective_value}"

            # Add node with label
            G.add_node(node_id, label=node_label)

            # Add edge if parent exists
            if parent_id is not None:
                G.add_edge(parent_id, node_id)

        # Use Graphviz hierarchical layout for better tree structure
        pos = graphviz_layout(G, prog="dot")

        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightblue", edgecolors="black", alpha=0.9)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color="gray", width=1.5, alpha=0.7)

        # Draw labels
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight="bold")

        # Set title
        plt.title("Branch & Bound Tree", fontsize=14, fontweight="bold")
        plt.axis("off")  # Hide axes

        # Save the plot
        plt.savefig(filename, bbox_inches="tight")
        plt.close()  # Close the plot after saving
