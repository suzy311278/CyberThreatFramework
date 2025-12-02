import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set backend to Agg for headless environments
import matplotlib.pyplot as plt
import networkx as nx
import os

class ThreatVisualizer:
    def __init__(self, log_dir=None):
        if log_dir is None:
            # Default to absolute path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(base_dir, "logs")
            
        self.log_file = os.path.join(log_dir, "simulation_log.csv")
        
    def plot_activity(self):
        if not os.path.exists(self.log_file):
            print("No logs found.")
            return

        try:
            df = pd.read_csv(self.log_file)
            if df.empty:
                print("Log file is empty.")
                return
                
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            # Plot 1: Events per Module
            plt.figure(figsize=(10, 6))
            df['Module'].value_counts().plot(kind='bar', color='skyblue')
            plt.title('Events per Module')
            plt.xlabel('Module')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig(os.path.join(os.path.dirname(self.log_file), 'events_per_module.png'))
            print(f"Generated events_per_module.png in {os.path.dirname(self.log_file)}")
            
            # Plot 2: Timeline of Events
            # Resample needs a datetime index
            plt.figure(figsize=(12, 6))
            df.set_index('Timestamp')['Module'].resample('1min').count().plot()
            plt.title('Event Frequency Over Time')
            plt.xlabel('Time')
            plt.ylabel('Events per Minute')
            plt.tight_layout()
            plt.savefig(os.path.join(os.path.dirname(self.log_file), 'timeline.png'))
            print(f"Generated timeline.png in {os.path.dirname(self.log_file)}")
            
        except Exception as e:
            print(f"Error generating plots: {e}")

    def plot_attack_graph(self):
        if not os.path.exists(self.log_file):
            return

        try:
            df = pd.read_csv(self.log_file)
            if df.empty:
                return
                
            G = nx.DiGraph()
            
            # We want to show the sequence of events, but group repeated ones
            # e.g. Start -> Attempt -> Failed (x3) -> Success -> End
            
            nodes = []
            last_event_type = None
            repeat_count = 0
            
            # Filter to only show the current attack session
            # We assume a new session starts with an event named "Start"
            # Find the index of the last "Start" event
            start_indices = df[df['Event'] == 'Start'].index
            
            if not start_indices.empty:
                last_start_idx = start_indices[-1]
                df = df.loc[last_start_idx:]
            else:
                # Fallback: just take the last 50 events if no Start found
                if len(df) > 50:
                    df = df.tail(50)
            
            # Grouping logic
            nodes = []
            last_event_type = None
            repeat_count = 0
            
            for index, row in df.iterrows():
                module = row['Module']
                event = row['Event']
                event_signature = f"{module}\n{event}"
                
                if event_signature == last_event_type:
                    repeat_count += 1
                    continue
                else:
                    if last_event_type:
                        label = last_event_type
                        if repeat_count > 0:
                            label += f"\n(x{repeat_count + 1})"
                        nodes.append(label)
                    last_event_type = event_signature
                    repeat_count = 0
            
            if last_event_type:
                label = last_event_type
                if repeat_count > 0:
                    label += f"\n(x{repeat_count + 1})"
                nodes.append(label)
            
            # Limit to last 10 nodes to prevent overcrowding
            if len(nodes) > 10:
                nodes = nodes[-10:]
            
            # Build Graph
            for i in range(len(nodes)):
                G.add_node(nodes[i])
                if i > 0:
                    G.add_edge(nodes[i-1], nodes[i])
            
            # Horizontal Layout (Compact)
            plt.figure(figsize=(12, 4)) # Wider to prevent overlap
            
            # Manually calculate positions to guarantee no overlap
            # Evenly spaced on X axis, all on Y=0
            pos = {}
            for i, node in enumerate(nodes):
                pos[node] = (i * 2, 0) # Multiply by 2 to give more space between nodes
            
            # Draw Edges
            nx.draw_networkx_edges(G, pos, 
                                 edge_color='#b71c1c', 
                                 width=2, 
                                 arrowsize=20, 
                                 arrowstyle='-|>',
                                 node_size=3000)
            
            # Draw Labels
            # Use a smaller font if text is long
            nx.draw_networkx_labels(G, pos, 
                                    font_size=8, 
                                    font_color='white',
                                    font_weight='bold',
                                    bbox=dict(facecolor='#d32f2f', edgecolor='black', boxstyle='round,pad=0.5')
                                    )
            
            # Adjust margins
            plt.xlim(-1, (len(nodes) * 2) - 1)
            plt.ylim(-1, 1)
            
            plt.title("Recent Attack Activity", color='#b71c1c', fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            
            output_path = os.path.join(os.path.dirname(self.log_file), 'attack_flow.png')
            plt.savefig(output_path, facecolor='white', bbox_inches='tight', dpi=100)
            print(f"Generated attack_flow.png in {os.path.dirname(self.log_file)}")
            plt.close()
            
        except Exception as e:
            print(f"Error generating graph: {e}")

if __name__ == "__main__":
    viz = ThreatVisualizer()
    viz.plot_activity()
    viz.plot_attack_graph()
